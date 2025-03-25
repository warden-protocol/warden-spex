import json
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

TypeSolverInput = TypeVar("TypeSolverInput", bound=BaseModel)
TypeSolverOutput = TypeVar("TypeSolverOutput", bound=BaseModel)
T = TypeVar("T", bound=BaseModel)


class MyBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")  # noqa: F841

    def pprint(self):
        print(self.__class__.__name__ + json.dumps(self.model_dump(), indent=4, default=str))


class SolverRequest(MyBaseModel, Generic[TypeSolverInput]):
    """
    Request for a solver, with inputs and quality guarantees.
    """

    model_config = ConfigDict(extra="forbid")

    solverInput: TypeSolverInput | None = None
    falsePositiveRate: float = Field(default=0.01, ge=0, le=1)


class SolverProof(MyBaseModel):
    """
    Solver proof as bloom filter and number of inserted items.
    """

    model_config = ConfigDict(extra="forbid")

    bloomFilter: bytes = b"BgAAAAAAAADYxCJU"
    countItems: int = Field(default=1, ge=0)


class SolverResponse(MyBaseModel, Generic[TypeSolverOutput]):
    """
    Solver response with output and proof.
    """

    model_config = ConfigDict(extra="forbid")

    solverOutput: TypeSolverOutput | None = None
    solverProof: SolverProof = SolverProof()


class VerifierRequest(MyBaseModel, Generic[TypeSolverOutput]):
    """
    Verifier request, with solver request and solver proof as
    input, as well as `verificationRatio` to control the minimum required confidence.
    """

    model_config = ConfigDict(extra="forbid")

    solverRequest: SolverRequest = SolverRequest()
    solverOutput: TypeSolverOutput | None = None
    solverProof: SolverProof = SolverProof()
    verificationRatio: float = Field(default=0.1, ge=0, le=1)


class VerifierResponse(MyBaseModel):
    """
    Verifier response, with number of verified items and
    the verification outcome.
    """

    model_config = ConfigDict(extra="forbid")

    countItems: int = Field(default=1, ge=0)
    isVerified: bool = False
    evidence: str | None = None


class Task(Generic[TypeSolverInput, TypeSolverOutput], ABC):
    """
    Abstract class for solver tasks (solver, verifier).
    """

    @staticmethod
    @abstractmethod
    def solve(request: SolverRequest[TypeSolverInput]) -> SolverResponse[TypeSolverOutput]:  # noqa: F841
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def verify(request: VerifierRequest) -> VerifierResponse:  # noqa: F841
        raise NotImplementedError
