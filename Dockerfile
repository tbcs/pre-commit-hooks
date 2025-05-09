# syntax=docker/dockerfile:1

# ==============================================================================
# intermediate images
# ==============================================================================

FROM library/eclipse-temurin:21-jdk-alpine AS jdk-builder

RUN apk add git maven

# ------------------------------------------------------------------------------

FROM jdk-builder AS googlejavaformat

ARG googlejavaformat_version=1.26.0  # https://github.com/google/google-java-format/releases/
ARG googlejavaformat_sha256sum=02a361357297fa962918c1d08830d50b17d62984d2a8649159b95b9a6d9f82b2

# Note on native image for google-java-format:
#
#     As of v1.23.0 the native image of google-java-format created by GraalVM v21.0.2 (with Docker
#     image ghcr.io/graalvm/native-image-community:21-muslib via `native-image --no-fallback
#     --static --libc=musl --strict-image-heap -jar google-java-format.jar -o google-java-format`)
#     cannot be used reliably.  Running the binary with `--help` works just fine, but invoking it to
#     actually format files fails with an exception.

ADD --checksum=sha256:${googlejavaformat_sha256sum} \
    https://github.com/google/google-java-format/releases/download/v${googlejavaformat_version}/google-java-format-${googlejavaformat_version}-all-deps.jar \
    /tmp/google-java-format.jar
RUN chmod 644 /tmp/google-java-format.jar

# ------------------------------------------------------------------------------

FROM jdk-builder AS ktfmt

ARG ktfmt_version=0.54  # https://github.com/facebook/ktfmt/releases/
ARG ktfmt_sha256sum=5e7eb28a0b2006d1cefbc9213bfc73a8191ec2f85d639ec4fc4ec0cd04212e82

# Note on native image for ktfmt:
#
#     As of v0.46 the native image of ktfmt created by GraalVM v21.0.1 cannot be used reliably.
#     Running the binary with `--help` works just fine, but invoking it to actually format files
#     fails with an exception.  This project relies a lot on reflection (apparently due to the
#     underlying Kotlin compiler), which poses a challenge for native compilation.  Others have
#     tried and failed:
#
#     https://github.com/facebook/ktfmt/issues/44
#     https://github.com/oracle/graal/issues/2824#issuecomment-685159371

ADD --checksum=sha256:${ktfmt_sha256sum} \
    https://repo1.maven.org/maven2/com/facebook/ktfmt/${ktfmt_version}/ktfmt-${ktfmt_version}-jar-with-dependencies.jar \
    /tmp/ktfmt.jar
RUN chmod 644 /tmp/ktfmt.jar

# ==============================================================================
# final image
# ==============================================================================

FROM library/eclipse-temurin:21-jdk-alpine

ARG commitlint_version=19.8.0  # https://github.com/conventional-changelog/commitlint/releases
ARG commitlint_config_version=19.8.0  # https://www.npmjs.com/package/@commitlint/config-conventional
ARG prettier_version=3.5.3  # https://github.com/prettier/prettier/releases
ARG prettierphp_version=0.22.4  # https://github.com/prettier/plugin-php/releases

# install base dependencies
RUN apk --no-cache add bash git

# install Node.js (dependency for various formatters)
RUN apk --no-cache add nodejs npm

# install shell script linter "shellcheck"
RUN apk --no-cache add shellcheck

# install shell script formatter "shfmt"
RUN apk --no-cache add shfmt

# install package containing "xmllint"
RUN apk --no-cache add libxml2-utils

# install google-java-format
COPY --from=googlejavaformat /tmp/google-java-format.jar /usr/local/lib/google-java-format.jar

# install ktfmt
COPY --from=ktfmt /tmp/ktfmt.jar /usr/local/lib/ktfmt.jar

# install code formatter 'prettier'
RUN npm install --global --omit=dev \
    prettier@${prettier_version} \
    && npm cache clean --force

# install PHP code formatter plugin for prettier
RUN npm install --global --omit=dev \
    @prettier/plugin-php@${prettierphp_version} \
    && npm cache clean --force

# install commitlint
RUN npm install --global --omit=dev \
    @commitlint/cli@${commitlint_version} \
    @commitlint/read@${commitlint_version} \
    @commitlint/config-conventional@${commitlint_config_version} \
    && npm cache clean --force

COPY hooks/ /hooks

WORKDIR /

ENV NODE_PATH=/usr/local/lib/node_modules

# ENTRYPOINT and/or CMD are expected to be set for each hook individually when invoked. Reset both
# here so that an error is raised by Docker if no override was specified.
ENTRYPOINT []
CMD []
