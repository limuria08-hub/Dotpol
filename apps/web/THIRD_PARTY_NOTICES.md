# Dotpol Web — Third-party UI package ledger

These are **runtime dependencies**, not copied upstream source trees or new backends.
The package manager must preserve the upstream licence files in installed packages.
The exact npm package versions, React 19 build and browser integration are checked
in the Phase 1 pull request. Review exact tarballs and generated deployment
attribution before publishing a distributable release.

| Component | Installed version | SPDX licence | Upstream | Scope |
|---|---|---|---|---|
| react-resizable-panels | 2.1.9 | MIT | https://github.com/bvaughn/react-resizable-panels | Desktop chat/artifact pane splitter only; keyboard resizing and local layout preference |
| lucide-react | 0.469.0 | ISC (some icon designs derive from Feather/MIT) | https://github.com/lucide-icons/lucide | Visual icons on the splitter and artifact-opening action |

The Lucide/Feather attribution and ISC/MIT licence obligations remain applicable
when publishing compiled icons. See https://lucide.dev/license and upstream
licence files for the full texts. These packages do not store political data,
invoke AI providers, access source evidence or contact hosted services.

**Status:** exact top-level dependencies pinned in `apps/web/package.json`.
A full npm dependency lockfile, automated transitive licence inventory,
SBOM/security audit and redistributable NOTICE check are **outstanding release
gates**; this ledger is not a complete supply-chain audit. Do not count
shadcn/ui, Radix, assistant-ui, Lexical, Perspective or Kepler as installed.
