import psyneulink as pnl

Inner_Composition = pnl.Composition(name="Inner Composition")

E = pnl.TransferMechanism(
    name="E",
    function=pnl.Linear(default_variable=[[0]]),
    termination_measure=pnl.Distance(
        metric=pnl.MAX_ABS_DIFF, default_variable=[[[0]], [[0]]]
    ),
)
F = pnl.TransferMechanism(
    name="F",
    function=pnl.Linear(default_variable=[[0]]),
    termination_measure=pnl.Distance(
        metric=pnl.MAX_ABS_DIFF, default_variable=[[[0]], [[0]]]
    ),
)

Inner_Composition.add_node(E)
Inner_Composition.add_node(F)

Inner_Composition.add_projection(
    projection=pnl.MappingProjection(
        name="MappingProjection from E[RESULT] to F[InputPort-0]",
        function=pnl.LinearMatrix(matrix=[[1.0]]),
    ),
    sender=E,
    receiver=F,
)


Inner_Composition.scheduler.termination_conds = {
    pnl.TimeScale.RUN: pnl.Never(),
    pnl.TimeScale.TRIAL: pnl.AllHaveRun(),
}
