MESON ?= meson

CONFIG ?= debug                      # debug | release | debugoptimized | plain | minsiz
BUILD_ROOT ?= build
BUILD_DIR := $(strip $(BUILD_ROOT)/$(CONFIG))

MESON_ARGS ?=
EXE ?= template

.PHONY: setup reconfigure build test run docs clean wipe status

setup:
	$(MESON) setup $(BUILD_DIR) --buildtype=$(CONFIG) $(MESON_ARGS)

reconfigure:
	$(MESON) setup --reconfigure $(BUILD_DIR) --buildtype=$(CONFIG) $(MESON_ARGS)

build: setup
	$(MESON) compile -C $(BUILD_DIR)

test: build
	$(MESON) test -C $(BUILD_DIR) --print-errorlogs

run: build
	./$(BUILD_DIR)/$(EXE) $(ARGS)

docs: setup
	$(MESON) compile -C $(BUILD_DIR) docs

clean:
	$(MESON) compile -C $(BUILD_DIR) --clean

wipe:
	rm -rf $(BUILD_ROOT)

status:
	$(MESON) configure $(BUILD_DIR)
