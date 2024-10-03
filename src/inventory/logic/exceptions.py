class InventoryLogicException(Exception):
    """All logic exceptions must be inherited from this class."""


class ItemBindingException(InventoryLogicException):
    """Raise if it is impossible to bind item with product."""


class ListingEditingException(InventoryLogicException):
    """Raise if it is impossible to add to listing."""


class AutosyncSetterException(InventoryLogicException):
    """Raise if it is impossible to set autosync flag."""
