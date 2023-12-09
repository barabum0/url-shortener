from fastapi import APIRouter
import importlib
import pkgutil

router = APIRouter()

package_name = "url_shortener.routers.api"
package = importlib.import_module(package_name)

routers = []

for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    module = importlib.import_module(f"{package_name}.{module_name}")
    if "router" in dir(module):
        routers.append(getattr(module, "router"))

for r in routers:
    router.include_router(r)
