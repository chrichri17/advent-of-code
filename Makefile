
.PHONY: aot
aot:
	@python3 main.py -i test

.PHONY: aoc
aoc:
	@python3 main.py -i in

.PHONY: next-day
next-day:
	@python3 make_next_day.py name
