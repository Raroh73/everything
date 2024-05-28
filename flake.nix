{
  description = "Everything";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
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
      in
      {
        devShells.default = pkgs.mkShell {
          name = "everything";

          packages = [
            pkgs.python3
            pkgs.python3Packages.channels
            pkgs.python3Packages.daphne
            pkgs.python3Packages.django
            pkgs.python3Packages.markdown
            pkgs.python3Packages.openai
            pkgs.tailwindcss
          ];
        };
      }
    );
}
