.PHONY: changelog lint release help

changelog: ## Show changelog since last version tag
	@tag=$$(git tag --sort=-version:refname --list 'v[0-9]*.[0-9]*.[0-9]*' | head -1) && \
	echo "## Changelog since $$tag" && \
	echo "" && \
	git log --oneline $$tag..HEAD | sed 's/^/- /'

lint: ## Run linting checks
	@echo "Running linting checks..."
	@uv run ruff check . --diff

release: lint ## Create a release. Usage: make release LEVEL=patch|minor|major
	@if [ -z "$(LEVEL)" ]; then \
		echo "Error: LEVEL is required. Usage: make release LEVEL=patch|minor|major"; \
		exit 1; \
	fi
	@CHANGELOG=$$($(MAKE) --no-print-directory changelog) && \
	echo "$$CHANGELOG" && \
	echo "Updating $(LEVEL) version..." && \
	uv run bumpver update --$(LEVEL) && \
	CURRENT_VERSION=$$(uv run bumpver show | grep "Current Version:" | cut -d' ' -f3) && \
	echo "Creating release tag v$$CURRENT_VERSION..." && \
	git tag "v$$CURRENT_VERSION" && \
	git push origin --tags && \
	if gh pr view --base main --head dev > /dev/null 2>&1; then \
		echo "PR already exists, skipping PR creation."; \
	else \
		gh pr create --base main --head dev \
			--title "Sync dev to main after release v$$CURRENT_VERSION" \
			--body "$$(printf '%s' "$$CHANGELOG")"; \
	fi && \
	echo "Release pushed successfully!"

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*##"}; {printf "  %-20s %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
