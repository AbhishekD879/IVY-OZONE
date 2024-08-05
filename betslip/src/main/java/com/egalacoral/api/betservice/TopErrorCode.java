//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for topErrorCode.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="topErrorCode">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="ACCOUNT_ERROR"/>
 *     &lt;enumeration value="BET_ERROR"/>
 *     &lt;enumeration value="CHANGE_ERROR"/>
 *     &lt;enumeration value="EVENT_ERROR"/>
 *     &lt;enumeration value="INTERNAL_ERROR"/>
 *     &lt;enumeration value="VALIDATION_ERROR"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "topErrorCode")
@XmlEnum
public enum TopErrorCode {

    ACCOUNT_ERROR,
    BET_ERROR,
    CHANGE_ERROR,
    EVENT_ERROR,
    INTERNAL_ERROR,
    VALIDATION_ERROR;

    public String value() {
        return name();
    }

    public static TopErrorCode fromValue(String v) {
        return valueOf(v);
    }

}
