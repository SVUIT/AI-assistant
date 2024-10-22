# Stage 1: Build
FROM ruby:3.2.3 AS build

WORKDIR /mmtt

# Copy the Gemfile and Gemfile.lock to leverage caching
COPY Gemfile Gemfile.lock ./

# Install Bundler and project dependencies
RUN gem install bundler && bundle install 

# Copy the entire project after installing dependencies
COPY . .

# Clean unnecessary files that are not required for the final image
RUN rm -rf node_modules tmp/cache app/assets vendor/assets spec

# Build Jekyll site (assuming you are using Jekyll)
RUN bundle exec jekyll build --destination _site

# Stage 2: Final image
FROM alpine:latest

WORKDIR /mmtt

# Install necessary system packages
RUN apk update && apk add --no-cache \
    ruby \
    ruby-dev \
    build-base \
    libffi-dev \
    zlib-dev \
    yaml-dev \
    libc-dev \
    linux-headers \
    readline-dev \
    libxml2-dev \
    libxslt-dev

# Copy the built site from the build stage to the final image
COPY --from=build /mmtt/_site /mmtt

# Install Bundler and Jekyll in the final image
RUN gem install bundler jekyll:4.3.3 webrick

EXPOSE 4000

# Start Jekyll server
CMD ["jekyll", "serve", "--source", "/mmtt", "--host", "0.0.0.0"]
