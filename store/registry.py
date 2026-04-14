from store.tools import (
    search_products,
    check_stock,
    recommend_products,
    track_order,
    place_order,
    cancel_order,
)

TOOLS = {
    "search_products": search_products,
    "check_stock": check_stock,
    "recommend_products": recommend_products,
    "track_order": track_order,
    "place_order": place_order,
    "cancel_order": cancel_order,
}
