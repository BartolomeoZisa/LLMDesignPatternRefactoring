from src.modules.responseStrategies import * 
import inspect


class ResponseStrategyRegistry:
    _strategies = {}

    @classmethod
    def register(cls, name):
        def decorator(strategy_cls):
            key = name.lower()
            cls._strategies[key] = strategy_cls
            return strategy_cls
        return decorator

    @classmethod
    def get_strategy_class(cls, name):
        key = name.lower()
        if key not in cls._strategies:
            raise ValueError(f"Unsupported strategy: {name}")
        return cls._strategies[key]

    @classmethod
    def get_default_model(cls, name):
        strategy_cls = cls.get_strategy_class(name)
        init_sig = inspect.signature(strategy_cls.__init__)
        param = init_sig.parameters.get("model_name")
        if param is not None and param.default is not inspect.Parameter.empty:
            return param.default



class ResponseFactory:
    @staticmethod
    def get_strategy(strategy_name, **kwargs):
        strategy_cls = ResponseStrategyRegistry.get_strategy_class(strategy_name)

        # Inject default model from class if not provided
        if "model_name" not in kwargs or not kwargs["model_name"]:
            default_model = ResponseStrategyRegistry.get_default_model(strategy_name)
            if default_model:
                kwargs["model_name"] = default_model

        # Filter only constructor-accepted args
        sig = inspect.signature(strategy_cls.__init__)
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}

        return strategy_cls(**filtered_kwargs)
