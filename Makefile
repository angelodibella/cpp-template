BUILDS = compile build clean

.PHONY := $(BUILDS)

.DEFAULT_GOAL := compile

compile:
	meson compile -C build

build:
	meson setup build

clean:
	rm -rf build
