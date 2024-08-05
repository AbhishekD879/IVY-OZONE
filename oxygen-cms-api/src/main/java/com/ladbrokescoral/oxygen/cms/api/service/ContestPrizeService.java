package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestPrizeRepository;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/** Contest Prizes Service */
@Service
@Slf4j
public class ContestPrizeService extends AbstractService<ContestPrize> {

  private ContestPrizeRepository contestPrizesRepository;
  private final String svgMenuPath;
  private final ImageService imageService;
  private final SvgImageParser svgImageParser;
  private String freebetOfferId;

  @Autowired
  public ContestPrizeService(
      ContestPrizeRepository contestPrizesRepository,
      @Value("${images.svg.path}") String svgMenuPath,
      ImageService imageService,
      SvgImageParser svgImageParser,
      @Value("${crm.freebet.offerId}") String freebetOfferId) {
    super(contestPrizesRepository);
    this.contestPrizesRepository = contestPrizesRepository;
    this.svgMenuPath = svgMenuPath;
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.freebetOfferId = freebetOfferId;
  }

  /**
   * List Contest Prizes based on Contest Id
   *
   * @param contestId - Contest Id by which Contest Prizes are retrived
   */
  public List<ContestPrize> getByContestId(String contestId) {
    List<ContestPrize> contestPrizes = contestPrizesRepository.findByContestId(contestId);
    for (ContestPrize contestPrize : contestPrizes) {
      log.info("freebetOfferId:{}", contestPrize.getFreebetOfferId());
      if ((("Freebet".equalsIgnoreCase(contestPrize.getType())
              || ("Ticket".equalsIgnoreCase(contestPrize.getType())))
          && StringUtils.isEmpty(contestPrize.getFreebetOfferId()))) {
        contestPrize.setFreebetOfferId(freebetOfferId);
      }
    }
    return contestPrizes;
  }

  public List<ContestPrize> getByContestIdAndBrand(String contestId, String brand) {
    return contestPrizesRepository.findOneByIdAndAndBrand(contestId, brand);
  }

  /**
   * Handle Uploading content of Contest Prizes
   *
   * @param id - Id of the Contest Prizes record which has to be updated
   * @param contestprizesIcon - Contest prize Icon
   * @param contestprizesSignPosting - Contest Prize Sign Posting
   */
  public ContestPrize handleFileUploading(
      String id, MultipartFile contestprizesIcon, MultipartFile contestprizesSignPosting) {
    ContestPrize contestPrizes = findOne(id).orElseThrow(NotFoundException::new);
    handleContestPrizesIcon(contestprizesIcon, contestPrizes);
    handleContestPrizesSignPostingIcon(contestprizesSignPosting, contestPrizes);
    save(contestPrizes);
    return contestPrizes;
  }

  /**
   * Handle Uploading SVG Icons of Contest Prizes
   *
   * @param contestPrizes - Contest Prizes Object
   * @param contestPrizesIcon - Icon
   */
  private void handleContestPrizesIcon(
      MultipartFile contestPrizesIcon, ContestPrize contestPrizes) {
    if (contestPrizesIcon != null) {
      Filename svgIconFile = getUploadedSvg(contestPrizes.getBrand(), contestPrizesIcon);
      contestPrizes.setIcon(svgIconFile);
    }
  }

  /**
   * Handle Uploading Sign Posting SVG Icons of Contest Prizes
   *
   * @param contestPrizes - Contest Prizes Object
   * @param contestPrizesSignPosting - Icon
   */
  private void handleContestPrizesSignPostingIcon(
      MultipartFile contestPrizesSignPosting, ContestPrize contestPrizes) {
    if (contestPrizesSignPosting != null) {
      Filename signpostingFile = getUploadedSvg(contestPrizes.getBrand(), contestPrizesSignPosting);
      contestPrizes.setSignPosting(signpostingFile);
    }
  }

  /**
   * Handle Uploading SVG images of Contest Prizes
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
   * Handle Delete SVG images of Contest Prizes
   *
   * @param id - Id of the Image
   * @param imageType - Image Type
   */
  public ContestPrize handleFileDelete(String id, String imageType) {
    ContestPrize contestPrizes = findOne(id).orElseThrow(NotFoundException::new);

    String svgPath;
    switch (ContestImageType.valueOf(imageType)) {
      case ICONFILE:
        svgPath = contestPrizes.getIcon().relativePath();
        contestPrizes.setIcon(null);
        break;
      case SIGHPOSTINGFILE:
        svgPath = contestPrizes.getSignPosting().relativePath();
        contestPrizes.setSignPosting(null);
        break;
      default:
        throw new UnsupportedOperationException("Unknown image type: " + imageType);
    }

    save(contestPrizes);

    imageService.removeImage(contestPrizes.getBrand(), svgPath);
    return contestPrizes;
  }

  /**
   * Checking for valid entries
   *
   * @param entity
   * @return
   */
  private boolean checkForValidEntries(@Valid ContestPrize entity) {
    boolean isValid = false;
    if (entity.getNumberOfEntries() != null) {
      if (!entity.getNumberOfEntries().contains("-")) {
        isValid = true;
      }
      if (entity.getNumberOfEntries().contains("-") && !entity.getNumberOfEntries().contains("*")) {
        isValid = true;
      } else if (hasStringLiterals(entity)) {
        String numberOfEntries = entity.getNumberOfEntries().replaceAll("\\s+", "");
        entity.setNumberOfEntries(numberOfEntries);
        isValid = true;
      }
    } else {
      isValid = true;
    }

    return isValid;
  }

  private boolean hasStringLiterals(ContestPrize contestPrize) {
    String numberOfEntries = contestPrize.getNumberOfEntries();
    return numberOfEntries.contains("-")
        && numberOfEntries.contains("*")
        && numberOfEntries.contains(",");
  }

  /**
   * Checking for valid field
   *
   * @param entity
   * @return
   */
  private boolean checkForValidField(@Valid ContestPrize entity) {
    boolean isValid = false;
    if (entity.getPercentageOfField() != null) {
      if (!entity.getPercentageOfField().contains("-")
          && !entity.getPercentageOfField().contains("*")) {
        isValid = true;
      } else if (!entity.getPercentageOfField().contains("-")
          && entity.getPercentageOfField().contains("*")) {
        if (entity.getPercentageOfField().contains(",")) {
          String percentageField = entity.getPercentageOfField().replaceAll("\\s+", "");
          entity.setPercentageOfField(percentageField);
          isValid = true;
        }
      }
      if (entity.getPercentageOfField().contains("-")
          && !entity.getPercentageOfField().contains("*")) {
        isValid = true;
      } else if (hasStringLiteralsForField(entity)) {
        String percentageField = entity.getPercentageOfField().replaceAll("\\s+", "");
        entity.setPercentageOfField(percentageField);
        isValid = true;
      }
    } else {
      isValid = true;
    }

    return isValid;
  }

  private boolean hasStringLiteralsForField(ContestPrize contestPrize) {
    String percentageField = contestPrize.getPercentageOfField();
    return percentageField.contains("-")
        && percentageField.contains("*")
        && percentageField.contains(",");
  }

  /**
   * checking for valid prize
   *
   * @param entity
   * @return
   */
  @Override
  public ContestPrize prepareModelBeforeSave(ContestPrize entity) {
    adjustDecimal(entity);
    boolean isValidEntry = checkForValidEntries(entity);
    boolean isValidField = checkForValidField(entity);
    if (isValidEntry && isValidField) {
      return entity;
    } else {
      throw new BadRequestException("Bad Request check the format of #entries or %field");
    }
  }

  private void adjustDecimal(ContestPrize entity) {
    if (entity.getValue() != null) {
      double modifiedValue = Double.parseDouble(entity.getValue());
      if (modifiedValue % 1.0 > 0) {
        entity.setValue(String.format("%.2f", modifiedValue));
      } else {
        Integer prizeValue = (int) Double.parseDouble(entity.getValue());
        entity.setValue(String.valueOf(prizeValue));
      }
    } else {
      entity.setValue("");
    }
  }

  /**
   * List ContestPrizes based on Brand
   *
   * @param brand - brand
   */
  public List<ContestPrize> findAllByBrandSorted(String brand) {
    return contestPrizesRepository.findByBrand(brand);
  }
}
