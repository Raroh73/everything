{
  description = "Everything";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    {
      self,
      flake-utils,
      nixpkgs,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        hatch = pkgs.hatch.overrideAttrs (oa: {
          disabledTests = oa.disabledTests ++ [
            "test_field_complex"
            "test_field_readme"
            "test_field_string"
            "test_plugin_dependencies_unmet"
          ];
        });
      in
      {
        devShells.default = pkgs.mkShell {
          name = "everything";

          packages = [
            hatch
            pkgs.python3
            pkgs.ruff
            pkgs.tailwindcss
          ];
        };
      }
    );
}
