//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:48:45 PM EEST 
//


package com.egalacoral.api.ws.identity;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for CredentialsType.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="CredentialsType">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="VERIFY_IDENTITY_TOKEN"/>
 *     &lt;enumeration value="VERIFY_USER_PASSWORD"/>
 *     &lt;enumeration value="VERIFY_CERTIFICATE"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "CredentialsType")
@XmlEnum
public enum CredentialsType {

    VERIFY_IDENTITY_TOKEN,
    VERIFY_USER_PASSWORD,
    VERIFY_CERTIFICATE;

    public String value() {
        return name();
    }

    public static CredentialsType fromValue(String v) {
        return valueOf(v);
    }

}