patch:
	bumpversion patch
	rm -rf -v dist/*
	poetry build
	poetry publish
