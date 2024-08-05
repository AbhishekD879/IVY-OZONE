//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:52:26 PM EEST 
//


package com.egalacoral.api.ws.authentication;

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
 *         &lt;element name="subject" type="{http://webservice.authnReqApi.securityframework.sportsbook.openbet.com/authn}user"/>
 *         &lt;element name="authenticationType" type="{http://webservice.authnReqApi.securityframework.sportsbook.openbet.com/authn}userType"/>
 *         &lt;element name="delegates" type="{http://webservice.authnReqApi.securityframework.sportsbook.openbet.com/authn}delegate" minOccurs="0"/>
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
    "subject",
    "authenticationType",
    "delegates"
})
@XmlRootElement(name = "getAuthnRequest")
public class GetAuthnRequest {

    @XmlElement(required = true)
    protected User subject;
    @XmlElement(required = true)
    protected UserType authenticationType;
    protected Delegate delegates;

    /**
     * Gets the value of the subject property.
     * 
     * @return
     *     possible object is
     *     {@link User }
     *     
     */
    public User getSubject() {
        return subject;
    }

    /**
     * Sets the value of the subject property.
     * 
     * @param value
     *     allowed object is
     *     {@link User }
     *     
     */
    public void setSubject(User value) {
        this.subject = value;
    }

    /**
     * Gets the value of the authenticationType property.
     * 
     * @return
     *     possible object is
     *     {@link UserType }
     *     
     */
    public UserType getAuthenticationType() {
        return authenticationType;
    }

    /**
     * Sets the value of the authenticationType property.
     * 
     * @param value
     *     allowed object is
     *     {@link UserType }
     *     
     */
    public void setAuthenticationType(UserType value) {
        this.authenticationType = value;
    }

    /**
     * Gets the value of the delegates property.
     * 
     * @return
     *     possible object is
     *     {@link Delegate }
     *     
     */
    public Delegate getDelegates() {
        return delegates;
    }

    /**
     * Sets the value of the delegates property.
     * 
     * @param value
     *     allowed object is
     *     {@link Delegate }
     *     
     */
    public void setDelegates(Delegate value) {
        this.delegates = value;
    }

}