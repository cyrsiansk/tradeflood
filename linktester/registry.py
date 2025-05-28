from typing import Type, Dict, Tuple, TypeVar

F = TypeVar("F")
C = TypeVar("C")


class LinkRegistry:
    def __init__(self):
        self._links: Dict[Tuple[Type, Type], Type] = {}

    def register(self, fetcher_cls: Type[F], candle_cls: Type[C], interface_cls: Type):
        self._links[(fetcher_cls, candle_cls)] = interface_cls

    def find_interface(self, fetcher_instance: F, candle_cls: Type[C]):
        key = (type(fetcher_instance), candle_cls)
        if key not in self._links:
            raise ValueError(f"No interface registered for: {key}")
        return self._links[key]


registry = LinkRegistry()


def link(fetcher_cls: Type[F], candle_cls: Type[C]):
    def decorator(interface_cls: Type):
        registry.register(fetcher_cls, candle_cls, interface_cls)
        return interface_cls

    return decorator


def InterfaceSearcher(fetcher_instance: F, candle_cls: Type[C]):
    interface_cls = registry.find_interface(fetcher_instance, candle_cls)
    instance = interface_cls()
    instance.history_fetcher = fetcher_instance
    return instance
