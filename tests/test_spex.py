import random

import numpy as np
from pydantic import BaseModel, PositiveInt

from warden_spex.models import SolverProof, SolverRequest, SolverResponse, Task, VerifierRequest, VerifierResponse
from warden_spex.spex import Blossom


class SolverInputPrimeSum(BaseModel):
    no_of_primes: PositiveInt = 10


class SolverOutputPrimeSum(BaseModel):
    sum_of_primes: PositiveInt = 129


class SolverRequestPrimeSum(SolverRequest[SolverInputPrimeSum]):
    solverInput: SolverInputPrimeSum = SolverInputPrimeSum()


class SolverResponsePrimeSum(SolverResponse[SolverOutputPrimeSum]):
    solverOutput: SolverOutputPrimeSum = SolverOutputPrimeSum()


class PrimeSumTask(Task[SolverInputPrimeSum, SolverOutputPrimeSum]):
    """
    Implementation of PrimeSum Task (lazy verifier).
    """

    @staticmethod
    def ith_prime(i: PositiveInt) -> PositiveInt:
        """
        Given `i` >= 1 , return the i-th prime.
        """
        assert i >= 1
        count, num = 0, 1
        while count < i:
            num += 1
            for d in range(2, int(num**0.5) + 1):
                if num % d == 0:
                    break
            else:
                count += 1
        return num

    @staticmethod
    def solve(request: SolverRequest[SolverInputPrimeSum]) -> SolverResponsePrimeSum:
        """
        PrimeSum-solver:
        Given a request to compute the sum of the first $n$ prime numbers, it returns
        the result along with a cryptographic proof of the performed computation.
        """

        # Compute primes and their sum
        assert isinstance(request.solverInput, SolverInputPrimeSum)
        primes = [PrimeSumTask.ith_prime(i) for i in range(1, request.solverInput.no_of_primes + 1)]
        sum_of_primes = sum(primes)
        print(f"Primes: {primes} sum: {sum_of_primes}")

        # Creating the Bloom filter by inserting all primes
        n_items = len(primes)
        blossom = Blossom(expected_items=n_items, false_positive_rate=request.falsePositiveRate)
        for prime in primes:
            blossom.add(np.array(prime))

        # Assembling the response
        return SolverResponsePrimeSum(
            solverOutput=SolverOutputPrimeSum(sum_of_primes=sum_of_primes),
            solverProof=SolverProof(countItems=blossom.inserted_items, bloomFilter=blossom.dump()),
        )

    @staticmethod
    def verify(request: VerifierRequest[SolverInputPrimeSum]) -> VerifierResponse:
        """
        PrimeSum-verifier-L: Verifier for lazy solvers.
        """

        # Load Bloom filter
        blossom = Blossom.load(request.solverProof)

        # Verify rate of false positives
        if not blossom.verify_false_positive_rate(expected_rate=request.solverRequest.falsePositiveRate):
            return VerifierResponse(isVerified=False, evidence="Failed false positive rate")

        # Verify number of items inserted in Bloom filter
        assert isinstance(request.solverRequest.solverInput, SolverInputPrimeSum)
        if blossom.inserted_items != request.solverRequest.solverInput.no_of_primes:
            return VerifierResponse(isVerified=False, evidence="Failed expected insertions in Bloom filter")

        # Verify random sample of items
        count_samples = int(np.ceil(request.solverProof.countItems * request.verificationRatio))
        primes_i = random.sample(list(range(1, request.solverRequest.solverInput.no_of_primes + 1)), count_samples)
        count_lookups = 0
        for i in primes_i:
            count_lookups += 1
            if not blossom.is_hit(np.array(PrimeSumTask.ith_prime(i))):
                return VerifierResponse(countItems=count_lookups, isVerified=False, evidence=f"Missing prime i={i}")

        return VerifierResponse(countItems=count_lookups, isVerified=True)


def test_spex():
    # Test: we can call the solver and the verifier tasks.

    task = PrimeSumTask()

    print("---- solver ----")

    no_of_primes = 10
    solver_input = SolverInputPrimeSum(no_of_primes=no_of_primes)

    solver_request = SolverRequest(
        solverInput=solver_input,
        falsePositiveRate=0.01,
    )

    solver_request.pprint()
    solver_response = task.solve(solver_request)
    solver_response.pprint()
    assert solver_response.solverProof.countItems == no_of_primes

    print("---- verification ----")

    verifier_request = VerifierRequest(
        solverRequest=solver_request,
        solverOutput=solver_response.solverOutput,
        solverProof=solver_response.solverProof,
        verificationRatio=0.3,
    )

    verifier_request.pprint()
    verify_request = task.verify(verifier_request)
    verify_request.pprint()

    assert verify_request.countItems == 3
    assert verify_request.isVerified is True
