//! Explicit runtime degradation policy. No cognition lives here.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RuntimeCondition {
    Healthy,
    ThermalPressure,
    MemoryPressure,
    NpuUnavailable,
    FirmwareInvalid,
    AuthorityDenied,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DegradationAction {
    Continue,
    ReduceWork,
    ShedNonEssentialBuffers,
    FallbackCpu,
    BlockExecution,
    FailClosed,
}

pub fn decide(condition: RuntimeCondition) -> DegradationAction {
    match condition {
        RuntimeCondition::Healthy => DegradationAction::Continue,
        RuntimeCondition::ThermalPressure => DegradationAction::ReduceWork,
        RuntimeCondition::MemoryPressure => DegradationAction::ShedNonEssentialBuffers,
        RuntimeCondition::NpuUnavailable => DegradationAction::FallbackCpu,
        RuntimeCondition::FirmwareInvalid => DegradationAction::BlockExecution,
        RuntimeCondition::AuthorityDenied => DegradationAction::FailClosed,
    }
}
