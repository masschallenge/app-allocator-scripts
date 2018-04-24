from app_allocator.classes.feature import Feature


class UniversalFeature(Feature):
    def initial_options(self, judges, startups):
        return []

    def option_counts(self, _):
        return [(spec.option, spec.count) for spec in self.option_specs]
