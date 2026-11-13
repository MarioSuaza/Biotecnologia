{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
      system = "x86_64-linux";
    in {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          git # Version control and publish to GitHub
          just # Task runner
          rsync # Publish to remote host
          quarto # For preview and render
          typst # Optional: Rendering exams
          ripgrep # Optional: Used for some just tasks
        ];
      };
    };
}
