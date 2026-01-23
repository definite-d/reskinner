# bump and tag version
bump-patch:
	@echo "Updating patch version..."
	bumpver update --patch

bump-minor:
	@echo "Updating minor version..."
	bumpver update --minor

bump-major:
	@echo "Updating major version..."
	bumpver update --major

# generate changelog since last version tag
changelog:
	@echo "## Changelog since $(shell git describe --tags --match 'v[0-9]*.[0-9]*.[0-9]*' --abbrev=0)" && \
	echo "" && \
	git log --oneline $(shell git describe --tags --match 'v[0-9]*.[0-9]*.[0-9]*' --abbrev=0)..HEAD | sed 's/^/- /'

# run linting checks
lint:
	@echo "Running linting checks..."
	uv run ruff check . --diff

# push tag and create PR (for when we've already bumped the version)
push-release:
	@echo "Creating release tag with v prefix..."
	git tag "v$(shell bumpver get current)" $(shell bumpver get current)
	@echo "Pushing tags to trigger build..."
	git push origin --tags
	@echo "Creating PR to sync dev to main..."
	gh pr create --base main --head dev --title "Sync dev to main after release" --body "Automated PR to sync dev branch changes to main after release v$(shell bumpver get current)\n\n## Changelog\n$$(make changelog)"
	@echo "Release pushed successfully!"

# create release with specified level: make release LEVEL=patch|minor|major
release: lint
	@echo "Creating release..."
	@echo "Changelog for this release:" && \
	$(MAKE) changelog
	@read -p "Continue with release? [y/N] " confirm && \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
		echo "Release cancelled."; exit 1; \
	fi
	@echo "Updating $(LEVEL) version..."
	bumpver update --$(LEVEL)
	$(MAKE) push-release