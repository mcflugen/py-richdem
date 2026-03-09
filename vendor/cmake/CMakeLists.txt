cmake_minimum_required(VERSION 3.15)

project(
  richdem
  DESCRIPTION "High-performance terrain analysis"
  LANGUAGES CXX
)

include_guard(GLOBAL)
include(GNUInstallDirs)

# ---
# Build defaults
# ---
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(BUILD_SHARED_LIBS "Build shared libraries" OFF)

if(APPLE)
  set(CMAKE_MACOSX_RPATH ON)
endif()

if(WIN32)
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

set(RICHDEM_DIR "${CMAKE_CURRENT_LIST_DIR}/../richdem")

# ---
# OpenMP
# ---
if(APPLE AND DEFINED ENV{OPENMP_PREFIX})
  set(OpenMP_ROOT "$ENV{OPENMP_PREFIX}")
endif()

find_package(OpenMP REQUIRED)
set(RICHDEM_OPENMP_ENABLED ${OpenMP_FOUND})

# ---
# richdem version info from git
# ---
find_package(Git QUIET)

set(RICHDEM_GIT_HASH "unknown")
set(RICHDEM_GIT_TAG  "unknown")
set(RICHDEM_GIT_DESC "unknown")

if(GIT_FOUND)
  execute_process(
    COMMAND "${GIT_EXECUTABLE}" -C "${RICHDEM_DIR}" rev-parse --short HEAD
    OUTPUT_VARIABLE RICHDEM_GIT_HASH
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
  )
  execute_process(
    COMMAND "${GIT_EXECUTABLE}" -C "${RICHDEM_DIR}" describe --tags --abbrev=0
    OUTPUT_VARIABLE RICHDEM_GIT_TAG
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
  )
  execute_process(
    COMMAND "${GIT_EXECUTABLE}" -C "${RICHDEM_DIR}" describe --tags --always --dirty
    OUTPUT_VARIABLE RICHDEM_GIT_DESC
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
  )
endif()

message(STATUS "RICHDEM_GIT_HASH = ${RICHDEM_GIT_HASH}")
message(STATUS "RICHDEM_GIT_TAG  = ${RICHDEM_GIT_TAG}")
message(STATUS "RICHDEM_GIT_DESC = ${RICHDEM_GIT_DESC}")

set(GENERATED_INCLUDE_DIR "${CMAKE_CURRENT_BINARY_DIR}/include")
set(GENERATED_HDR "${GENERATED_INCLUDE_DIR}/richdem/build_config.hpp")

file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/include/richdem")

configure_file(
  "${CMAKE_CURRENT_LIST_DIR}/build_config.hpp.in"
  "${GENERATED_HDR}"
  @ONLY
)

# ---
# librichdem
# ---
string(TIMESTAMP RICHDEM_TIMESTAMP UTC)

add_library(richdem
  "${RICHDEM_DIR}/src/richdem.cpp"
  "${RICHDEM_DIR}/src/random.cpp"
  "${RICHDEM_DIR}/src/terrain_generation/terrain_generation.cpp"
  "${RICHDEM_DIR}/src/terrain_generation/PerlinNoise.cpp"
)

set_target_properties(richdem PROPERTIES
  POSITION_INDEPENDENT_CODE ON
)

target_include_directories(richdem
  PUBLIC
    $<BUILD_INTERFACE:${RICHDEM_DIR}/include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_link_libraries(richdem
  PRIVATE
    OpenMP::OpenMP_CXX
)

target_compile_definitions(richdem
  PUBLIC
    RICHDEM_NO_PROGRESS
    RICHDEM_GIT_HASH="${RICHDEM_GIT_HASH}"
    RICHDEM_GIT_TAG="${RICHDEM_GIT_TAG}"
    RICHDEM_GIT_DESC="${RICHDEM_GIT_DESC}"
    RICHDEM_COMPILE_TIME="${RICHDEM_TIMESTAMP}"
)

# ---
# Install
# ---
install(
  TARGETS richdem
  EXPORT richdemTargets
  ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
  LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
  RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
)

install(
  DIRECTORY "${RICHDEM_DIR}/include/richdem"
  DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)

install(
  DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/include/richdem"
  DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)

install(
  EXPORT richdemTargets
  NAMESPACE richdem::
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/richdem"
)
