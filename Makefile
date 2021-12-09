run:
ifndef TOKEN
	$(error TOKEN is not set)
endif
	@ python src/main.py --config ./config.yaml --token ${TOKEN}
