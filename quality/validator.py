import great_expectations as gx

class DataQualityGuard: def init(self, context_path: str): self.context = gx.get_context(context_root_dir=context_path)

def validate_batch(self, batch_data, expectation_suite_name: str):
    """
    Runs automated quality checks. 
    If validation fails, the record is quarantined.
    """
    validator = self.context.get_validator(
        batch_request=batch_data,
        expectation_suite_name=expectation_suite_name
    )
    results = validator.validate()
    
    if not results["success"]:
        # Logic for quarantine and alerting
        return False, results["statistics"]
    return True, None