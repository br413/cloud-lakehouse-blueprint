from src.lakehouse.deploy import build_deployment_plan, build_rollback_plan


def test_deployment_and_rollback_plans(blueprint) -> None:
    deploy = build_deployment_plan(blueprint)
    rollback = build_rollback_plan(deploy)
    assert deploy[0].action.startswith("terraform apply")
    assert len(deploy) == len(rollback)
    assert rollback[0].order >= rollback[-1].order
