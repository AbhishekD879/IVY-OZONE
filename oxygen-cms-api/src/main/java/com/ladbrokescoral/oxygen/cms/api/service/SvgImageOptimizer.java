package com.ladbrokescoral.oxygen.cms.api.service;

import java.io.File;
import java.nio.file.Files;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.buildobjects.process.ProcBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;

@Slf4j
@Service
public class SvgImageOptimizer {

  private static final String SVGO_DISABLE_PLUGINS =
      "{removeUselessDefs,cleanupIDs,removeViewBox,removeAttrs}";
  private static final String SVGO_ENABLE_PLUGINS = "{prefixIds}";
  private static final String SVGO_PLUGINS_CONFIG =
      "{\"plugins\":[{\"prefixIds\":{\"prefix\":\"%s\"}}]}";

  private boolean enableOptimization;

  @Autowired
  public SvgImageOptimizer(@Value("${images.svg.optimization.enable}") boolean enableOptimization) {
    this.enableOptimization = enableOptimization;
  }

  public Optional<String> optimize(String svg) {

    if (!enableOptimization) {
      return Optional.ofNullable(svg);
    }

    String stdOut = null;
    File svgoConfigFile = null;

    try {
      String md5OfSVGContent = DigestUtils.md5DigestAsHex(svg.getBytes());
      // Don't need it to be long, think first 8 from MD5 will reduce collision in CSS class-names
      String svgoConfig = String.format(SVGO_PLUGINS_CONFIG, md5OfSVGContent.substring(0, 8));

      svgoConfigFile = File.createTempFile(md5OfSVGContent, ".json");
      Files.write(svgoConfigFile.toPath(), svgoConfig.getBytes());

      stdOut =
          new ProcBuilder("svgo")
              .withArgs(
                  String.format("--config=%s", svgoConfigFile.getAbsolutePath()),
                  String.format("--enable=%s", SVGO_ENABLE_PLUGINS),
                  String.format("--disable=%s", SVGO_DISABLE_PLUGINS),
                  String.format("--string=%s", svg.replace("\n", "")))
              .run()
              .getOutputString();
      log.debug("Process StdOut - {}", stdOut);
    } catch (Exception e) {
      log.error("Process failed - {}", e.toString());
    } finally {
      if (Objects.nonNull(svgoConfigFile)) {
        svgoConfigFile.delete();
      }
    }

    return Optional.ofNullable(stdOut).filter(s -> !s.isEmpty());
  }
}
