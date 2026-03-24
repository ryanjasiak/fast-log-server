cmake_minimum_required(VERSION 3.28)

project(fast-log-server)


add_executable(server)

target_sources(server PRIVATE
    src/main.cpp
)

set_target_properties(server PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin"
)