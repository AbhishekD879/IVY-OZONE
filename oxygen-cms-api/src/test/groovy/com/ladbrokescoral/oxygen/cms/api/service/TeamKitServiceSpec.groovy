package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.*
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException
import com.ladbrokescoral.oxygen.cms.api.repository.TeamKitRepository
import org.springframework.mock.web.MockMultipartFile
import org.springframework.web.multipart.MultipartFile
import spock.lang.Specification

class TeamKitServiceSpec extends Specification {

  private TeamKitRepository repository = Mock(TeamKitRepository)
  private ImageService imageService = Mock(ImageService)
  private SvgImageParser svgImageService = Mock(SvgImageParser)
  private String teamKitPath = "/images/team-kit/"

  private final TeamKitService service = new TeamKitService(repository, imageService, svgImageService, teamKitPath)
  private final String brand = "bma"
  private final String fullTeamKitPath = teamKitPath + brand


  def "Delete"() {
    given:
    repository.findById("123") >> Optional.of(new TeamKit(brand, "testName", "/testPath", "", ""))
    imageService.removeImage(brand, "testPath") >> Boolean.TRUE
    GameEvent gameEvent = new GameEvent()
    Team team = new Team()
    team.setName("teamA")
    team.setTeamKitIcon("/testPath")
    gameEvent.setHome(team)

    when:
    service.delete("123")

    then:
    1 * repository.deleteById("123")
  }

  def "UploadImage"() {
    TeamKit teamKit = new TeamKit(brand, "testName", "/testPath", "", "")

    Filename filename = new Filename()
    filename.setPath("/testPath")
    filename.setOriginalname("test.png")

    MultipartFile image = new MockMultipartFile("test.png", "test.png", "", new byte[0])
    given:
    repository.findById("123") >> Optional.of(teamKit)
    imageService.upload(brand, image, fullTeamKitPath, "test", null) >> Optional.of(filename)

    when:
    def result = service.uploadImage(image, new TeamKit(brand, "MU", "test", "", ""))

    then:
    result.getPath() == "/testPath/test.png"
    result.getTeamName() == "MU"
  }

  def "Upload - error"() {
    given:
    MultipartFile image = new MockMultipartFile("test.png", "test.png", "", new byte[0])
    repository.findById("123") >> Optional.of(new TeamKit())
    imageService.upload(brand, image, fullTeamKitPath, "test", null) >> Optional.empty()
    when:
    TeamKit teamKit = new TeamKit(brand, "Man Unt", "test", "", "")
    teamKit.setId("123")
    service.uploadImage(image, teamKit)
    then:
    thrown(IllegalStateException)
  }

  def "Save TeamKit"() {
    given:
    Team team = new Team()
    team.setName("MU")
    team.setTeamKitIcon("/test/path/icon.svg")
    Svg svg = new Svg()
    svg.setSvg("svg")
    svg.setSvg("svgId")
    TeamKit teamKit = new TeamKit(brand, team.getName(), team.getTeamKitIcon(), svg.getSvg(), svg.getId())
    repository.save(teamKit) >> teamKit
    when:
    def kit = service.saveTeamKit(team, svg, brand)
    then:
    kit.getSvg() == svg.getSvg()
    kit.getPath() == team.getTeamKitIcon()
  }

  def "Upload svg image"() {
    given:
    teamKitPath = "/images/team-kit"
    TeamKit teamKit = new TeamKit(brand, "MU", "/images/team-kit/icon.svg", "svg", "svgId")
    Svg svg = new Svg()
    svg.setSvg("svg")
    svg.setSvg("svgId")
    MultipartFile image = new MockMultipartFile("icon.svg", "icon.svg", "", new byte[0])

    Filename filename = new Filename()
    filename.setPath("/images/team-kit")
    filename.setOriginalname("icon.svg")
    filename.setFilename("icon.svg")

    repository.findById("123") >> Optional.of(teamKit)
    svgImageService.parse(image) >> Optional.of(svg)
    imageService.upload(brand, image, fullTeamKitPath, "icon", null) >> Optional.of(filename)
    repository.findAll() >> Collections.emptyList()

    when:
    def kit = service.uploadSvgImage(image, "123")

    then:
    kit.getSvg() == svg.getSvg()
    kit.getSvgId() == svg.getId()
    kit.getTeamName() == teamKit.getTeamName()
    kit.getPath() == teamKit.getPath()
  }

  def "Upload svg image (already existed in TeamKit collection)"() {
    given:
    TeamKit teamKit = new TeamKit(brand, "MU", "/images/team-kit/icon.svg", "svg", "svgId")
    Svg svg = new Svg()
    svg.setSvg("svg")
    svg.setSvg("svgId")
    MultipartFile image = new MockMultipartFile("icon.svg", "icon.svg", "", new byte[0])

    Filename filename = new Filename()
    filename.setPath("/images/team-kit")
    filename.setOriginalname("icon.svg")
    filename.setFilename("icon1.svg")

    repository.findById("123") >> Optional.of(teamKit)
    svgImageService.parse(image) >> Optional.of(svg)
    imageService.upload(brand, image, fullTeamKitPath, "icon1", null) >> Optional.of(filename)
    repository.findAll() >> Collections.singletonList(teamKit)

    when:
    def kit = service.uploadSvgImage(image, "123")

    then:
    kit.getSvg() == svg.getSvg()
    kit.getSvgId() == svg.getId()
    kit.getTeamName() == teamKit.getTeamName()
    kit.getPath() == "/images/team-kit/icon1.svg"
  }

  def "Upload svg image - Validation Exception"() {
    given:
    TeamKit teamKit = new TeamKit(brand, "MU", "/images/team-kit/icon.svg", "svg", "svgId")
    MultipartFile image = new MockMultipartFile("icon.svg", "icon.svg", "", new byte[0])

    repository.findById("123") >> Optional.of(teamKit)
    svgImageService.parse(image) >> Optional.empty()

    when:
    service.uploadSvgImage(image, "123")

    then:
    thrown(ValidationException)
  }

  def "Create TeamKit"() {
    TeamKit teamKit = new TeamKit(brand, "MU", "/images/team-kit/icon.svg", "svg", "svgID")
    repository.save(teamKit) >> teamKit
    when:
    def kit = service.create(teamKit)
    then:
    kit.getSvg() == "svg"
    kit.getPath() == "/images/team-kit/icon.svg"
  }

  def "Validate OK"() {
    TeamKit teamKit = new TeamKit(brand, "MU", "/images/team-kit/icon.svg", "svg", "svgID")
    when:
    service.validate(teamKit)
    then:
    noExceptionThrown()
  }

  def "Validate No brand"() {
    TeamKit teamKit = new TeamKit("", "MU", "/images/team-kit/icon.svg", "svg", "svgID")
    when:
    service.validate(teamKit)
    then:
    def exception = thrown(ValidationException)
    exception.message.contains("Field brand is required and cannot be empty")
  }

  def "Validate No team name"() {
    TeamKit teamKit = new TeamKit(brand, "", "/images/team-kit/icon.svg", "svg", "svgID")
    when:
    service.validate(teamKit)
    then:
    def exception = thrown(ValidationException)
    exception.message.contains("Field teamName is required and cannot be empty")
  }

  def "Find All by team name and brand"() {
    List<TeamKit> teamKits = new ArrayList<>()
    teamKits.add(new TeamKit(brand, "MU", "/images/team-kit/icon.svg", "svg", "svgID"))
    teamKits.add(new TeamKit(brand, "MU", "/images/team-kit/icon1.svg", "svg", "svgID"))
    teamKits.add(new TeamKit(brand, "MU", "/images/team-kit/icon2.svg", "svg", "svgID"))
    given:
    repository.findByBrandAndTeamName(brand, "MU") >> teamKits
    when:
    def kits = service.findTeamKits(brand, "MU")
    then:
    kits.size() == 3
  }
}
