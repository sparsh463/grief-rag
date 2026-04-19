from grief_rag.models import Scenario


def test_top_responses_with_rankings():
    s = Scenario(
        id="gl_001",
        description="test",
        responses={"A": "resp_a", "B": "resp_b", "C": "resp_c"},
        rankings={"A": 2, "B": 1, "C": 3},
    )
    assert s.top_responses(2) == ["resp_b", "resp_a"]


def test_top_responses_unranked_returns_all():
    s = Scenario(
        id="gl_001",
        description="test",
        responses={"A": "resp_a", "B": "resp_b"},
        rankings=None,
    )
    assert set(s.top_responses()) == {"resp_a", "resp_b"}
