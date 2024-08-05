package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.ContestRequest;
import com.ladbrokescoral.oxygen.cms.api.dto.ContestStatus;
import com.ladbrokescoral.oxygen.cms.api.entity.Contest;
import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestRepository;
import com.ladbrokescoral.oxygen.cms.api.service.showdown.ShowdownService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.util.Base64;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import javax.xml.bind.DatatypeConverter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.web.multipart.MultipartFile;

/** Contests Service */
@Service
@Slf4j
public class ContestService extends SortableService<Contest> {

  private final ContestRepository contestsRepository;
  private final ShowdownService showdownService;
  private final String svgMenuPath;
  private final ImageService imageService;
  private final SvgImageParser svgImageParser;
  private final String longUrl;
  @Lazy @Autowired private SiteServeService siteServeService;
  private String freebetOfferId;
  private String ticketOfferId;
  private ContestPrizeService contestPrizesService;

  @Autowired
  public ContestService(
      ContestRepository contestsRepository,
      @Value("${images.svg.path}") String svgMenuPath,
      @Value("${magicurl.longurl}") String longUrl,
      ImageService imageService,
      SvgImageParser svgImageParser,
      ShowdownService showdownService,
      @Value("${crm.freebet.offerId}") String freebetOfferId,
      @Value("${crm.ticket.offerId}") String ticketOfferId,
      ContestPrizeService contestPrizesService) {
    super(contestsRepository);
    this.contestsRepository = contestsRepository;
    this.svgMenuPath = svgMenuPath;
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.showdownService = showdownService;
    this.longUrl = longUrl;
    this.freebetOfferId = freebetOfferId;
    this.ticketOfferId = ticketOfferId;
    this.contestPrizesService = contestPrizesService;
  }

  @Override
  public Contest prepareModelBeforeSave(Contest entity) {
    try {
      setContestId(entity);
      generateContestUrl(entity);
      return entity;
    } catch (Exception e) {
      log.error(e.getMessage(), e);
    }
    return entity;
  }

  /** Generate Ladbrokes contest URL */
  public Contest generateURL(Contest entity) {
    entity.setContestURL(new StringBuilder(this.longUrl).append(entity.getId()).toString());
    return entity;
  }

  /**
   * Handle Uploading content of Contests
   *
   * @param id - Id of the Contest record which has to be updated
   * @param contestLogo - Contest logo
   * @param contestIcon - Contest Icon
   */
  public Contest handleFileUploading(
      String id, MultipartFile contestLogo, MultipartFile contestIcon) {
    Contest contest = findOne(id).orElseThrow(NotFoundException::new);
    handleContestLogo(contestLogo, contest);
    handleContesticon(contestIcon, contest);
    save(contest);
    return contest;
  }

  /**
   * Handle Uploading contest Icons
   *
   * @param contest - Contest Object
   * @param contestIcon - Icon
   */
  private void handleContesticon(MultipartFile contestIcon, Contest contest) {
    if (contestIcon != null) {
      Filename contestIconFile = getUploadedSvg(contest.getBrand(), contestIcon);
      contest.setIcon(contestIconFile);
    }
  }

  /**
   * Handle Uploading Sponsor SVG logos of Contest
   *
   * @param contest - Contest Object
   * @param contestLogo - Logo
   */
  private void handleContestLogo(MultipartFile contestLogo, Contest contest) {
    if (contestLogo != null) {
      Filename contestLogoFile = getUploadedSvg(contest.getBrand(), contestLogo);
      contest.setSponsorLogo(contestLogoFile);
    }
  }

  /**
   * Handle Uploading SVG images of Contests
   *
   * @param brand - Brand
   * @param svg - Multipart File
   */
  private Filename getUploadedSvg(String brand, MultipartFile svg) {
    try {
      Optional<Svg> parsedSvg = svgImageParser.parse(svg);
      if (!parsedSvg.isPresent()) {
        throw new BadRequestException("Svg parsing error for image: " + svg.getOriginalFilename());
      }
    } catch (SvgImageParseException ex) {
      throw new BadRequestException("Svg parsing error for image: " + svg.getOriginalFilename());
    }

    return imageService
        .upload(brand, svg, svgMenuPath)
        .orElseThrow(
            () ->
                new FileUploadException(
                    "Image uploading error for image: " + svg.getOriginalFilename()));
  }

  /**
   * Handle Delete SVG images of Contests
   *
   * @param id - Id of the Image
   * @param imageType - Image Type
   */
  public Contest handleFileDelete(String id, String imageType) {
    Contest contest = findOne(id).orElseThrow(NotFoundException::new);

    String svgPath;
    switch (ContestImageType.valueOf(imageType)) {
      case CONTESTLOGO:
        svgPath = contest.getSponsorLogo().relativePath();
        contest.setSponsorLogo(null);
        break;
      case CONTESTICON:
        svgPath = contest.getIcon().relativePath();
        contest.setIcon(null);
        break;
      default:
        throw new UnsupportedOperationException("Unknown image type: " + imageType);
    }

    save(contest);

    imageService.removeImage(contest.getBrand(), svgPath);
    return contest;
  }

  /**
   * List Contest based on Brand
   *
   * @param brand - brand
   */
  public List<Contest> findAllByBrandSorted(String brand) {
    return contestsRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }

  public List<Contest> findAllByBrandAndEventId(String brand, String eventId) {
    return contestsRepository.findByBrandAndEventAndDisplayTrue(brand, eventId);
  }

  public List<Contest> getContestsByDate(Instant fromDate, Instant toDate) {
    return contestsRepository.findByStartDateBetween(fromDate, toDate);
  }

  public List<Contest> findByBrandAndDate(Instant fromDate, String brand) {
    return contestsRepository.findByBrandAndStartDateGreaterThan(brand, fromDate);
  }

  public List<Contest> getContestsByBrandAndEvents(String brand, List<String> eventIds) {
    return contestsRepository.findByBrandAndEventInAndDisplayTrue(brand, eventIds);
  }

  public List<Contest> getContestsByBrandAndDisplayTrue(String brand) {
    return contestsRepository.findByBrandAndDisplayTrue(brand);
  }

  /**
   * To check whether the event is completed or not to generate the report
   *
   * @param id
   * @return
   */
  public Contest checkForEventCompleted(String id) {
    log.info("Fetching the contest data for contestId {} ", id);
    Optional<Contest> optionalContest = findOne(id);
    if (optionalContest.isPresent()) {
      Contest contest = optionalContest.get();
      if (Objects.nonNull(contest.getEvent())) {
        Optional<ContestStatus> entriesCount =
            showdownService.getContestStatus(contest.getEvent(), contest.getId());
        if (entriesCount.isPresent()) {
          ContestStatus status = entriesCount.get();
          contest.setEntriesSize(String.valueOf(status.getEntriesSize()));
          contest.setReportGenerated(status.isReportGenerated());
          contest.setCompleted(status.isRegularTimeFinished());
        } else {
          log.info("Data is not present in ContestStatus for contestId:{}", contest.getId());
        }
      }
      return contest;
    } else {
      throw new NotFoundException();
    }
  }

  public Contest setContestWithOfferIds(Contest contest) {
    log.info("freebetOfferId:{},ticketOfferId:{}", freebetOfferId, ticketOfferId);
    contest.setFreebetOfferId(freebetOfferId);
    contest.setTicketOfferId(ticketOfferId);
    return contest;
  }

  public Contest setContestId(Contest contest) throws NoSuchAlgorithmException {
    if (org.apache.commons.lang.StringUtils.isBlank(contest.getId()))
      contest.setId(generateContestId(contest.getName()));
    return contest;
  }

  private String generateContestId(String contestName) throws NoSuchAlgorithmException {
    MessageDigest digest = MessageDigest.getInstance("SHA-256");
    String nowTime = Instant.now().toString() + contestName;
    byte[] rawdata = digest.digest(nowTime.getBytes(StandardCharsets.UTF_8));
    byte[] encoded = Base64.getEncoder().encode(rawdata);
    return DatatypeConverter.printBase64Binary(encoded);
  }

  /**
   * @param request
   * @param newContest
   */
  public void populateContestPrizes(ContestRequest request, Contest clonedContest) {
    List<ContestPrize> contestPrizes =
        contestPrizesService.getByContestId(request.getIntialContestId());
    if (!CollectionUtils.isEmpty(contestPrizes)) {
      contestPrizes.forEach(
          (ContestPrize prize) -> {
            ContestPrize clonedContestPrize = new ContestPrize();
            BeanUtils.copyProperties(prize, clonedContestPrize);
            clonedContestPrize.setId(null);
            clonedContestPrize.setContestId(clonedContest.getId());
            contestPrizesService.save(clonedContestPrize);
          });
    }
  }

  /**
   * @param request
   * @param newContest
   */
  public void generateContestUrl(Contest newContest) {
    if (newContest.isInvitationalContest()) {
      generateURL(newContest);
    }
  }
}
