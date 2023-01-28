from typing import Iterable

from cleo.helpers import argument
from poetry.console.commands.command import Command
from poetry.core.constraints.version import Version
from poetry.core.packages.package import Package
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.repositories.exceptions import PackageNotFound


class Main(Command):
    name = "watsin"

    description = "Shows the available `extras` in a particular poetry package"

    arguments = [
        argument(name="package_name", description="The name of the package"),
        argument(
            name="package_version",
            description=(
                "The version of the package."
                " If not provided will check the latest version"
            ),
            optional=True,
        ),
    ]

    def _fetch_latest_package(self, name: str) -> Package | None:
        packages = self.poetry.pool.search(name)
        if not (
            package := next(
                (package for package in packages if package.name == name), None
            )
        ):
            return None

        return self._find_package(package.name, package.version)

    def _find_package(self, name: str, version: Version | None) -> Package:
        if version:
            return self.poetry.pool.package(name, version)

        if package := self._fetch_latest_package(name):
            return package

        raise PackageNotFound(f"Package {name} ({version}) not found.")

    def _formatted_extras(self, package: Package) -> Iterable[str]:
        for extra, dependencies in package.extras.items():
            formatted_extra = f"<info>{extra}</> : \n"
            formatted_extra += "\n".join(
                f"   * {dependency.pretty_name} ({dependency.pretty_constraint})"
                for dependency in dependencies
            )

            yield formatted_extra

    def handle(self) -> int:
        package_name = self.argument("package_name")
        package_version = (
            Version.parse(raw_version)
            if (raw_version := self.argument("package_version"))
            else None
        )

        package = self._find_package(package_name, package_version)

        for formatted_extra in self._formatted_extras(package):
            self.line(formatted_extra)

        return 0


class Watsin(ApplicationPlugin):
    @property
    def commands(self) -> list[type[Command]]:
        return [Main]
