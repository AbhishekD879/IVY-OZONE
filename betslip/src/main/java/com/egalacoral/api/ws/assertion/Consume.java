//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:51:29 PM EEST 
//


package com.egalacoral.api.ws.assertion;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for anonymous complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="assertion" type="{http://www.w3.org/2001/XMLSchema}string"/>
 *         &lt;element name="delegateSessionToken" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "assertion",
    "delegateSessionToken"
})
@XmlRootElement(name = "consume", namespace = "http://webservice.acs.securityframework.sportsbook.openbet.com/authn")
public class Consume {

    @XmlElement(namespace = "http://webservice.acs.securityframework.sportsbook.openbet.com/authn", required = true)
    protected String assertion;
    @XmlElement(namespace = "http://webservice.acs.securityframework.sportsbook.openbet.com/authn")
    protected String delegateSessionToken;

    /**
     * Gets the value of the assertion property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAssertion() {
        return assertion;
    }

    /**
     * Sets the value of the assertion property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAssertion(String value) {
        this.assertion = value;
    }

    /**
     * Gets the value of the delegateSessionToken property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDelegateSessionToken() {
        return delegateSessionToken;
    }

    /**
     * Sets the value of the delegateSessionToken property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDelegateSessionToken(String value) {
        this.delegateSessionToken = value;
    }

}
