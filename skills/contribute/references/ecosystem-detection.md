# Ecosystem Detection Matrix & Command Lookup

This reference guides **Step 5** (Convention Gathering) and **Step 9** (Verification) of the `contribute` pipeline to identify the project's language, build system, test runner, and linter without guessing generic commands.

---

## Detection Matrix

| Language / Stack | Manifest / Indicator Files | Default Test Command | Default Lint / Format Command | Build Command |
|---|---|---|---|---|
| **JavaScript / TypeScript (pnpm)** | `pnpm-lock.yaml`, `package.json` | `pnpm test` (or `pnpm vitest run`) | `pnpm lint` / `pnpm prettier --check .` | `pnpm build` |
| **JavaScript / TypeScript (npm)** | `package-lock.json`, `package.json` | `npm test` (or `npx vitest run`) | `npm run lint` | `npm run build` |
| **JavaScript / TypeScript (yarn)** | `yarn.lock`, `package.json` | `yarn test` | `yarn lint` | `yarn build` |
| **JavaScript / TypeScript (bun)** | `bun.lockb` / `bun.lock`, `package.json` | `bun test` | `bun run lint` | `bun build` |
| **JavaScript / TypeScript (Biome)** | `biome.json`, `biome.jsonc` | runner per package manager | `pnpm biome check` (or `npx @biomejs/biome check`) | runner per package manager |
| **Deno 2.x** | `deno.json`, `deno.jsonc`, `deno.lock` | `deno test` | `deno lint` / `deno fmt --check` | `deno task build` |
| **Rust (Cargo / Nextest)** | `Cargo.toml`, `Cargo.lock` | `cargo nextest run` (fallback: `cargo test`) | `cargo clippy --all-targets -- -D warnings` / `cargo fmt --check` | `cargo build` |
| **Python (uv / pytest)** | `pyproject.toml`, `uv.lock` | `uv run pytest` | `uv run ruff check .` / `uv run ruff format --check .` | `uv build` |
| **Python (pixi)** | `pixi.toml`, `pixi.lock` | `pixi run test` | `pixi run lint` | `pixi run build` |
| **Python (Poetry)** | `pyproject.toml`, `poetry.lock` | `poetry run pytest` | `poetry run ruff check .` / `poetry run black --check .` | `poetry build` |
| **Python (pip / venv)** | `requirements.txt`, `setup.py` | `pytest` | `flake8` / `black --check .` | `python setup.py build` |
| **Go** | `go.mod`, `go.sum` | `go test -race ./...` | `golangci-lint run` / `go vet ./...` | `go build ./...` |
| **Zig** | `build.zig`, `build.zig.zon` | `zig test` | `zig fmt --check .` | `zig build` |
| **Elixir / Phoenix** | `mix.exs`, `mix.lock` | `mix test` | `mix credo` / `mix format --check-formatted` | `mix compile` |
| **Java / Kotlin (Gradle)** | `build.gradle`, `build.gradle.kts`, `gradlew` | `./gradlew test` | `./gradlew check` | `./gradlew build` |
| **Java (Maven)** | `pom.xml`, `mvnw` | `./mvnw test` (or `mvn test`) | `mvn checkstyle:check` | `mvn package` |
| **C / C++ (CMake)** | `CMakeLists.txt` | `ctest` | `clang-tidy` / `clang-format --dry-run` | `cmake --build build` |
| **Ruby** | `Gemfile`, `Gemfile.lock` | `bundle exec rspec` | `bundle exec rubocop` | `bundle exec rake build` |
| **PHP** | `composer.json`, `composer.lock` | `composer test` (or `vendor/bin/phpunit`) | `vendor/bin/phpcs` / `composer lint` | `composer install` |
| **Swift** | `Package.swift` | `swift test` | `swiftlint` | `swift build` |

---

## Monorepos & Task Orchestrators

When working inside a monorepo or project with an orchestrator, run targets through the orchestrator to preserve dependency graphs and caching:

| Orchestrator | Indicator Files | Scoped Test Command | Scoped Lint Command |
|---|---|---|---|
| **Turborepo** | `turbo.json` | `pnpm turbo run test --filter=<pkg>` | `pnpm turbo run lint --filter=<pkg>` |
| **Nx** | `nx.json` | `pnpm nx test <project>` | `pnpm nx lint <project>` |
| **Justfile** | `Justfile`, `justfile` | `just test` (check targets with `just -l`) | `just lint` |
| **Taskfile** | `Taskfile.yml`, `Taskfile.yaml` | `task test` (check targets with `task --list`) | `task lint` |
| **Lefthook** | `lefthook.yml` | `lefthook run pre-commit` (checks all staged hooks) | `lefthook run pre-commit` |
| **Pre-commit** | `.pre-commit-config.yaml` | `pre-commit run --all-files` | `pre-commit run --all-files` |

---

## Convention Lookup Hierarchy

When inspecting a target repository, discover the exact commands in this priority order:

1. **`CONTRIBUTING.md` / `DEVELOPMENT.md`:** Look for sections titled "Running Tests", "Local Development", or "Pre-PR Checklist".
2. **`package.json` / `Makefile` / `Taskfile.yml` / `Justfile`:** Read explicitly defined script targets (such as `make test`, `pnpm test:unit`).
3. **CI Configurations (`.github/workflows/*.yml`, `.gitlab-ci.yml`):** The CI scripts are the ultimate source of truth for what tests and linter flags must pass before merging.
4. **Toolchain Defaults:** Use the detection tables above only when no explicit script or CI workflow overrides it.

