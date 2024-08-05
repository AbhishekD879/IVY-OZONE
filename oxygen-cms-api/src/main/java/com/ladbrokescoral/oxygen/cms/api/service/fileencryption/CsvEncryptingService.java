package com.ladbrokescoral.oxygen.cms.api.service.fileencryption;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvParser;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;
import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.codec.Hex;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@RequiredArgsConstructor
public class CsvEncryptingService {

  private final MultipartFile file;
  private final String encryptingKey;
  private final CsvSchema csvSchema;
  private static final CsvMapper CSV_MAPPER = getCsvMapper();

  @SneakyThrows
  public MultipartFile getEncryptedContent() {
    return CSV_MAPPER
        .readerFor(String[].class)
        .with(csvSchema)
        .<String[]>readValues(file.getBytes())
        .readAll()
        .parallelStream()
        .flatMap(bytes -> Arrays.stream(bytes).parallel())
        .map(this::getHashedValue)
        .map(hash -> new String[] {hash})
        .collect(Collectors.collectingAndThen(Collectors.toList(), this::toCsvMultipartFile));
  }

  private String getHashedValue(String username) {
    String payload = username + encryptingKey;

    return new String(Hex.encode(getDigest().digest(payload.getBytes(StandardCharsets.UTF_8))));
  }

  @SneakyThrows
  private MultipartFile toCsvMultipartFile(List<String[]> content) {
    byte[] byteContent =
        CSV_MAPPER
            .writerFor(new TypeReference<List<String[]>>() {})
            .with(csvSchema)
            .writeValueAsBytes(content);

    return new EncryptedMultipartFile(byteContent, file);
  }

  private static CsvMapper getCsvMapper() {
    return new CsvMapper().enable(CsvParser.Feature.WRAP_AS_ARRAY);
  }

  @SneakyThrows
  private static MessageDigest getDigest() {
    return MessageDigest.getInstance("SHA-256");
  }

  @Slf4j
  @Data
  public static class EncryptedMultipartFile implements MultipartFile {
    private final byte[] content;
    private final MultipartFile originalFile;

    EncryptedMultipartFile(byte[] content, MultipartFile originalFile) {
      this.content = content;
      this.originalFile = originalFile;
    }

    @Override
    public String getName() {
      return originalFile.getName();
    }

    @Override
    public String getOriginalFilename() {
      return originalFile.getOriginalFilename();
    }

    @Override
    public String getContentType() {
      return originalFile.getContentType();
    }

    @Override
    public boolean isEmpty() {
      return content == null || content.length == 0;
    }

    @Override
    public long getSize() {
      return content.length;
    }

    @Override
    public byte[] getBytes() {
      return content;
    }

    @Override
    public InputStream getInputStream() {
      return new BufferedInputStream(new ByteArrayInputStream(content));
    }

    @Override
    public void transferTo(File dest) {
      try (FileOutputStream fileOutputStream = new FileOutputStream(dest)) {
        fileOutputStream.write(content);
      } catch (IOException e) {
        log.error("Error in transferring the received file to the given destination file", e);
      }
    }
  }
}
