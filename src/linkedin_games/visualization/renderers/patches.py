from .shikaku import ShikakuRenderer


class PatchesRenderer(ShikakuRenderer):
    def _set_grid(self) -> None:
        super()._set_grid()
