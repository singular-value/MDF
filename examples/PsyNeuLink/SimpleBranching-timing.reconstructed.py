import psyneulink as pnl

comp = pnl.Composition(name="comp")

A = pnl.TransferMechanism(
    name="A",
    function=pnl.Linear(default_variable=[[0]]),
    termination_measure=pnl.Distance(
        metric=pnl.MAX_ABS_DIFF, default_variable=[[[0]], [[0]]]
    ),
)
B = pnl.TransferMechanism(
    name="B",
    function=pnl.Linear(default_variable=[[0]]),
    termination_measure=pnl.Distance(
        metric=pnl.MAX_ABS_DIFF, default_variable=[[[0]], [[0]]]
    ),
)
C = pnl.TransferMechanism(
    name="C",
    function=pnl.Linear(default_variable=[[0]]),
    termination_measure=pnl.Distance(
        metric=pnl.MAX_ABS_DIFF, default_variable=[[[0]], [[0]]]
    ),
)
D = pnl.TransferMechanism(
    name="D",
    function=pnl.Linear(default_variable=[[0]]),
    termination_measure=pnl.Distance(
        metric=pnl.MAX_ABS_DIFF, default_variable=[[[0]], [[0]]]
    ),
)

comp.add_node(A)
comp.add_node(B)
comp.add_node(C)
comp.add_node(D)

comp.add_projection(
    projection=pnl.MappingProjection(
        name="MappingProjection from A[RESULT] to B[InputPort-0]",
        function=pnl.LinearMatrix(matrix=[[1.0]]),
    ),
    sender=A,
    receiver=B,
)
comp.add_projection(
    projection=pnl.MappingProjection(
        name="MappingProjection from B[RESULT] to C[InputPort-0]",
        function=pnl.LinearMatrix(matrix=[[1.0]]),
    ),
    sender=B,
    receiver=C,
)
comp.add_projection(
    projection=pnl.MappingProjection(
        name="MappingProjection from B[RESULT] to D[InputPort-0]",
        function=pnl.LinearMatrix(matrix=[[1.0]]),
    ),
    sender=B,
    receiver=D,
)

comp.scheduler.add_condition(A, pnl.TimeInterval(interval=7, unit="ms"))
comp.scheduler.add_condition(
    B,
    pnl.All(
        pnl.TimeInterval(interval=1, start=1, unit="ms"),
        pnl.Not(pnl.TimeInterval(interval=7, start=6, unit="ms")),
        pnl.Not(pnl.TimeInterval(interval=7, start=7, unit="ms")),
    ),
)
comp.scheduler.add_condition(C, pnl.TimeInterval(interval=7, start=6, unit="ms"))
comp.scheduler.add_condition(D, pnl.TimeInterval(interval=7, start=13, unit="ms"))

comp.scheduler.termination_conds = {
    pnl.TimeScale.RUN: pnl.Never(),
    pnl.TimeScale.TRIAL: pnl.AllHaveRun(),
}
