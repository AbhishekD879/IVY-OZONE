package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.Team;
import com.ladbrokescoral.oxygen.cms.api.entity.TeamKit;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.TeamKitRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.util.List;
import java.util.Optional;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Service
public class TeamKitService extends AbstractService<TeamKit> {

  private final ImageService imageService;
  private final SvgImageParser svgImageParser;
  private final String teamKitPath;
  private final TeamKitRepository teamKitRepository;

  public TeamKitService(
      TeamKitRepository teamKitRepository,
      ImageService imageService,
      SvgImageParser svgImageParser,
      @Value("${images.teamKit.path}") String teamKitPath) {
    super(teamKitRepository);
    this.teamKitRepository = teamKitRepository;
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.teamKitPath = teamKitPath;
  }

  @Override
  public void delete(String id) {
    TeamKit teamKit = findOne(id).orElseThrow(NotFoundException::new);

    String path = teamKit.getPath();
    if (StringUtils.isNotBlank(path)) {
      imageService.removeImage(teamKit.getBrand(), path.startsWith("/") ? path.substring(1) : path);
    }
    super.delete(id);
  }

  public TeamKit uploadImage(
      @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile image, TeamKit teamKit) {

    Filename file =
        imageService
            .upload(teamKit.getBrand(), image, path(teamKit), getFilename(image), null)
            .orElseThrow(() -> new IllegalStateException("Issue occurred during image uploading"));

    teamKit.setPath(PathUtil.normalizedPath(file.getPath(), file.getOriginalname()));

    return teamKit;
  }

  private String getFilename(@ValidFileType({"jpeg", "png", "jpg"}) MultipartFile image) {
    return Optional.ofNullable(image.getOriginalFilename())
        .filter(img -> img.contains("."))
        .map(img -> StringUtils.substringBefore(img, "."))
        .orElseGet(image::getOriginalFilename);
  }

  public TeamKit saveTeamKit(Team team, Svg svg, String brand) {
    return save(
        new TeamKit(brand, team.getName(), team.getTeamKitIcon(), svg.getSvg(), svg.getId()));
  }

  public TeamKit uploadSvgImage(@ValidFileType("svg") MultipartFile file, String id) {
    TeamKit teamKit = findOne(id).orElseThrow(NotFoundException::new);
    Optional<Svg> svg = svgImageParser.parse(file);
    if (!svg.isPresent()) {
      throw new ValidationException("Svg image is invalid");
    }

    String name = getFilename(file);
    name = validateImageNameOrElseGetNew(name);
    Filename filename =
        imageService
            .upload(teamKit.getBrand(), file, path(teamKit), name, null)
            .orElseThrow(() -> new IllegalStateException("Issue occurred during image uploading"));
    teamKit.setPath(PathUtil.normalizedPath(filename.getPath(), filename.getFilename()));
    teamKit.setSvg(svg.get().getSvg());
    teamKit.setSvgId(svg.get().getId());
    return teamKit;
  }

  public String validateImageNameOrElseGetNew(String name) {
    List<TeamKit> teamKits = findAll();
    Optional<String> sameImageName =
        teamKits.stream()
            .filter(teamKit -> StringUtils.isNotBlank(teamKit.getPath()))
            .map(teamKit -> teamKit.getPath().split("/"))
            .filter(items -> items.length > 0)
            .map(items -> items[items.length - 1])
            .filter(item -> item.contains("."))
            .map(item -> item.split("\\.")[0])
            .filter(item -> item.equals(name))
            .findFirst();
    if (sameImageName.isPresent()) {
      return name + 1; // added uniqueness to name
    }
    return name;
  }

  public TeamKit create(@Validated TeamKit entity) {
    return super.save(entity);
  }

  public void validate(TeamKit teamKit) {
    if (StringUtils.isBlank(teamKit.getBrand())) {
      throw new ValidationException("Field brand is required and cannot be empty");
    }
    if (StringUtils.isBlank(teamKit.getTeamName())) {
      throw new ValidationException("Field teamName is required and cannot be empty");
    }
  }

  public List<TeamKit> findTeamKits(String brand, String name) {
    return teamKitRepository.findByBrandAndTeamName(brand, name);
  }

  private String path(TeamKit teamKit) {
    return StringUtils.endsWith(teamKitPath, "/")
        ? (teamKitPath + teamKit.getBrand())
        : String.format("%s/%s", teamKitPath, teamKit.getBrand());
  }
}
