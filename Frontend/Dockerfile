# Stage 1: Build
FROM ruby:3.2.3 AS build

WORKDIR /mmtt

# Copy the Gemfile and Gemfile.lock
COPY Gemfile Gemfile.lock ./

# Install Bundler and project dependencies
RUN gem install bundler && bundle install

# Copy the project files after installing dependencies to leverage Docker caching
COPY . .

# Install Jekyll and build the site
RUN gem install jekyll && bundle exec jekyll build

# Stage 2: Final image
FROM alpine:latest

WORKDIR /mmtt

# Install necessary packages
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

# Copy only the built site from the build stage
COPY --from=build /mmtt/_site /mmtt

# Install Bundler and Jekyll in the final image
RUN gem install bundler jekyll:4.3.3 webrick

EXPOSE 4000

# Start Jekyll server
CMD ["jekyll", "serve", "--source", "/mmtt", "--host", "0.0.0.0"]
