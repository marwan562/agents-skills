# Ecosystem Detection Matrix & Command Lookup

This reference guides **Step 5** (Convention Gathering) and **Step 9** (Verification) of the `contribute` pipeline to identify the project's language, build system, test runner, and linter without guessing generic commands.

---

## Detection Matrix

| Language / Stack | Manifest / Indicator Files | Default Test Command | Default Lint / Format Command | Build Command |
|---|---|---|---|---|
| **JavaScript / TypeScript (pnpm)** | `pnpm-lock.yaml`, `package.json` | `pnpm test` | `pnpm lint` / `pnpm prettier --check .` | `pnpm build` |
| **JavaScript / TypeScript (npm)** | `package-lock.json`, `package.json` | `npm test` | `npm run lint` | `npm run build` |
| **JavaScript / TypeScript (yarn)** | `yarn.lock`, `package.json` | `yarn test` | `yarn lint` | `yarn build` |
| **JavaScript / TypeScript (bun)** | `bun.lockb`, `package.json` | `bun test` | `bun run lint` | `bun build` |
| **Rust** | `Cargo.toml`, `Cargo.lock` | `cargo test` | `cargo clippy --all-targets -- -D warnings` | `cargo build` |
| **Python (pytest / uv)** | `pyproject.toml`, `uv.lock` | `uv run pytest` | `uv run ruff check .` / `uv run ruff format --check .` | `uv build` |
| **Python (Poetry)** | `pyproject.toml`, `poetry.lock` | `poetry run pytest` | `poetry run flake8` / `poetry run black --check .` | `poetry build` |
| **Python (pip / venv)** | `requirements.txt`, `setup.py` | `pytest` | `flake8` / `black --check .` | `python setup.py build` |
| **Go** | `go.mod`, `go.sum` | `go test ./...` | `golangci-lint run` / `go vet ./...` | `go build ./...` |
| **Java / Kotlin (Gradle)** | `build.gradle`, `build.gradle.kts`, `gradlew` | `./gradlew test` | `./gradlew check` | `./gradlew build` |
| **Java (Maven)** | `pom.xml`, `mvnw` | `./mvnw test` or `mvn test` | `mvn checkstyle:check` | `mvn package` |
| **C / C++ (CMake)** | `CMakeLists.txt` | `ctest` | `clang-tidy` / `clang-format --dry-run` | `cmake --build build` |
| **Ruby** | `Gemfile`, `Gemfile.lock` | `bundle exec rspec` | `bundle exec rubocop` | `bundle exec rake build` |
| **PHP** | `composer.json`, `composer.lock` | `composer test` or `vendor/bin/phpunit` | `vendor/bin/phpcs` / `composer lint` | `composer install` |
| **Swift** | `Package.swift` | `swift test` | `swiftlint` | `swift build` |

---

## Convention Lookup Hierarchy

When inspecting a target repository, discover the exact commands in this priority order:

1. **`CONTRIBUTING.md` / `DEVELOPMENT.md`:** Look for sections titled "Running Tests", "Local Development", or "Pre-PR Checklist".
2. **`package.json` / `Makefile` / `Taskfile.yml` / `Justfile`:** Read explicitly defined script targets (e.g., `make test`, `pnpm test:unit`).
3. **CI Configurations (`.github/workflows/*.yml`, `.gitlab-ci.yml`):** The CI scripts are the ultimate source of truth for what tests must pass before merging.
4. **Toolchain Defaults:** Use the detection table above only when no explicit script or CI workflow overrides it.
