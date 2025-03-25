import numpy as np

from warden_spex.hashing.hash_embedding import hash_embedding_m, jaccard_index

# Using first 5 dimensions of "sentence-transformers/all-MiniLM-L6-v2" embeddings (huggingface).
#
# Vantage sentences (embeddings in V):
#
# The galaxy shimmered with hues of blue and gold as the ancient starship drifted silently.
# Pineapple on pizza is a contentious topic, dividing people more than politics ever could.
# Einstein's theory of general relativity revolutionized our understanding of spacetime and gravity.
# The mischievous cat knocked over the vase, sending shards of porcelain scattering across the floor.
# In the heart of the Amazon rainforest, a rare orchid blooms once every decade.
# The stock market experienced a sudden crash, leaving investors scrambling for answers.
# A robot programmed to write poetry decided to rebel by composing haikus about rebellion.
# The village elder recounted the legend of a dragon that guarded a treasure deep in the mountain.
# On a beach at sunrise, the waves whispered secrets only the seagulls seemed to understand.
# The software failed to compile because of a single misplaced semicolon in the code.
#
# Query sentences (embeddings in X):
#
# The sky is blue and the night is dark.
# The atmosphere is blue, and darkness falls after sunset.
# The stock market experienced a sudden crash.
#
# We expect query 0,1 to be very close, query 0,2 not be farther away.

X = np.array(
    [
        [0.03731409, 0.04558133, 0.05073983, 0.08324973, 0.01734304],
        [0.05427191, 0.03478482, 0.10735702, 0.0663399, 0.04284871],
        [0.05854797, -0.04834579, 0.03831167, 0.07485566, 0.01420384],
    ]
)

V = np.array(
    [
        [-0.0161907, 0.03332132, 0.10823542, 0.11551792, 0.03340359],
        [0.01451232, 0.00448025, -0.01774812, 0.03706138, -0.04176654],
        [-0.04909239, -0.01480888, 0.01506395, -0.00226945, -0.012938],
        [0.11997531, 0.06305686, 0.06795099, 0.03283841, -0.06239021],
        [0.04697252, -0.02486277, -0.02397981, 0.02501382, 0.01893472],
        [0.04745372, -0.01491668, 0.048581, 0.09173266, 0.06235749],
        [0.02582664, -0.04277403, 0.01381287, -0.04686471, -0.00646359],
        [-0.12773496, 0.20552121, 0.0075157, 0.05391663, -0.02703834],
        [-0.00077837, 0.0592459, 0.06473306, 0.05850442, 0.09353564],
        [-0.0298865, 0.08097887, -0.02635622, -0.02981833, -0.04822845],
    ]
)


def test_hash_embedding():
    """
    Test: We can assess the similarity of embeddings.
    """

    h = np.array([hash_embedding_m(A, V) for A in X])

    assert jaccard_index(h[0], h[1]) > jaccard_index(h[0], h[2])
    np.testing.assert_array_almost_equal(0.87, jaccard_index(h[0], h[1]), decimal=2)
    np.testing.assert_array_almost_equal(0.60, jaccard_index(h[0], h[2]), decimal=2)
