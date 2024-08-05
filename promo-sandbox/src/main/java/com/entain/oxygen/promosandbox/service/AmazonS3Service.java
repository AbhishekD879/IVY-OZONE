package com.entain.oxygen.promosandbox.service;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.S3Object;
import com.entain.oxygen.promosandbox.config.S3BrandProperties;
import com.entain.oxygen.promosandbox.dto.UserRankInfoDto;
import com.entain.oxygen.promosandbox.exception.PromoSandboxException;
import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.charset.CharsetDecoder;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.Row$;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.Metadata;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.retry.support.RetryTemplate;
import org.springframework.stereotype.Service;
import scala.collection.JavaConverters;

@Service
@Slf4j
public class AmazonS3Service {

  private final RetryTemplate retryTemplate;

  private final AmazonS3 amazonS3;

  private final S3BrandProperties s3BrandConfig;

  @Autowired
  public AmazonS3Service(
      RetryTemplate retryTemplate, AmazonS3 amazonS3, S3BrandProperties properties) {
    this.retryTemplate = retryTemplate;
    this.amazonS3 = amazonS3;
    this.s3BrandConfig = properties;
  }

  public UserRankInfoDto fetchAmazonS3CsvData(String promotionId, String filePath) {
    try {
      return retryTemplate.execute(context -> downloadCsvFile(filePath));
    } catch (Exception ex) {
      log.error(
          "Error while loading user data to spark. promotionId : {} : {} ",
          promotionId,
          ex.getMessage());
      return new UserRankInfoDto();
    }
  }

  private UserRankInfoDto downloadCsvFile(final String keyName) throws IOException {
    UserRankInfoDto responseDto = null;
    S3Object s3Object = null;
    try {
      long startTime = System.currentTimeMillis();
      s3Object = amazonS3.getObject(s3BrandConfig.getBucket(), keyName);
      responseDto = new UserRankInfoDto();
      responseDto.setLastFileModified(s3Object.getObjectMetadata().getLastModified().toInstant());
      CsvMapper mapper = new CsvMapper();
      CsvSchema schema = CsvSchema.emptySchema().withHeader();
      CharsetDecoder charsetDecoder = Charset.forName("windows-1252").newDecoder();
      List<Map<String, String>> dataList;
      try (InputStreamReader stream =
          new InputStreamReader(s3Object.getObjectContent(), charsetDecoder)) {
        MappingIterator<Map<String, String>> iterator =
            mapper.readerFor(LinkedHashMap.class).with(schema).readValues(stream);
        dataList = iterator.readAll();
      }

      log.info(
          "File Downloaded FileKeyName(Path) : {}, UserCount : {} ,TimeTaken(MILLISECOND) : {},lastFileUpdated:{} ",
          keyName,
          dataList.size(),
          (System.currentTimeMillis() - startTime),
          s3Object.getObjectMetadata().getLastModified());

      List<String> cols = new ArrayList<>(dataList.get(0).keySet());
      responseDto.setRowList(prepareRows(dataList, cols));
      responseDto.setStructType(prepareSchemas(cols));
      log.debug(
          "TimeTaken for downloading and processingData FileKeyName(Path) : {} ,TimeTaken(MILLISECOND) : {} ",
          keyName,
          (System.currentTimeMillis() - startTime));
    } catch (Exception ex) {
      log.error(
          "Error while retrieving data from amazon s3 fileKey:: {},error:{} ",
          keyName,
          ex.getMessage());
      throw new PromoSandboxException("Error while retrieving data from amazon s3");
    } finally {
      if (Objects.nonNull(s3Object)) {
        s3Object.close();
      }
    }
    return responseDto;
  }

  private List<Row> prepareRows(List<Map<String, String>> dataList, List<String> cols) {
    return dataList
        .parallelStream()
        .map(row -> cols.stream().map(c -> (Object) row.get(c)))
        .map(row -> row.collect(Collectors.toList()))
        .map(row -> JavaConverters.asScalaBufferConverter(row).asScala().toSeq())
        .map(Row$.MODULE$::fromSeq)
        .collect(Collectors.toList());
  }

  private StructType prepareSchemas(List<String> cols) {
    return new StructType(
        cols.stream()
            .map(c -> new StructField(c, DataTypes.StringType, true, Metadata.empty()))
            .toArray(StructField[]::new));
  }
}
