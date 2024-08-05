package com.ladbrokescoral.oxygen.cms.util;

import static java.util.stream.Collectors.joining;

import com.ladbrokescoral.oxygen.cms.api.exception.InvalidPathException;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.file.Paths;
import java.util.stream.Stream;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.lang3.StringUtils;

@Slf4j
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class PathUtil {

  private static final String PATH_SEPARATOR = "/";

  public static String concatUri(String basePath, String... relatedPath) {
    basePath = basePath.trim();
    if (!basePath.endsWith(PATH_SEPARATOR)) {
      basePath += PATH_SEPARATOR;
    }
    String path = concatPath(null, relatedPath);
    if (path.startsWith(PATH_SEPARATOR)) {
      path = path.substring(PATH_SEPARATOR.length());
    }

    return URI.create(basePath).resolve(path).toString();
  }

  public static String concatPath(String basePath, String... relatedPath) {
    String concatenatedPath =
        Stream.concat(Stream.of(basePath), Stream.of(relatedPath))
            .filter(StringUtils::isNotBlank)
            .collect(joining(PATH_SEPARATOR));
    return FilenameUtils.normalize(concatenatedPath, true);
  }

  public static String normalize(String input) {
    try {
      return new URI(input).normalize().toString();
    } catch (URISyntaxException e) {
      log.error("error while parsing path :: {}", e.getMessage());
      throw new InvalidPathException("Invalid path " + input);
    }
  }

  public static String normalizedPath(String uri, String filename) {
    return Paths.get(normalize(uri), normalize(filename)).toString();
  }
}
