//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import java.io.Serializable;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAnyAttribute;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.namespace.QName;


/**
 * <p>Java class for leg complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="leg">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="errorRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;choice>
 *           &lt;element name="sportsLeg" type="{http://schema.products.sportsbook.openbet.com/betcommon}sportsLeg"/>
 *           &lt;element name="manualLeg" type="{http://schema.products.sportsbook.openbet.com/betcommon}manualLeg"/>
 *           &lt;element name="poolLeg" type="{http://schema.products.sportsbook.openbet.com/betcommon}poolLeg"/>
 *           &lt;element name="lotteryLeg" type="{http://schema.products.sportsbook.openbet.com/betcommon}lotteryLeg"/>
 *         &lt;/choice>
 *         &lt;element name="noCombi" type="{http://schema.products.sportsbook.openbet.com/betcommon}noCombi" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attGroup ref="{http://schema.openbet.com/core}entityAttrGroup"/>
 *       &lt;attribute name="banker" type="{http://schema.openbet.com/core}yesNo" />
 *       &lt;attribute name="result" type="{http://schema.products.sportsbook.openbet.com/betcommon}betLegResult" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "leg", namespace = "http://schema.products.sportsbook.openbet.com/betcommon", propOrder = {
    "errorRef",
    "sportsLeg",
    "manualLeg",
    "poolLeg",
    "lotteryLeg",
    "noCombi"
})
public class Leg
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    protected List<EntityRef> errorRef;
    protected SportsLeg sportsLeg;
    protected ManualLeg manualLeg;
    protected PoolLeg poolLeg;
    protected LotteryLeg lotteryLeg;
    protected NoCombi noCombi;
    @XmlAttribute
    protected YesNo banker;
    @XmlAttribute
    protected String result;
    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String documentId;
    @XmlAttribute
    protected String provider;
    @XmlAttribute
    protected String addr;
    @XmlAttribute
    protected String version;
    @XmlAttribute
    @XmlSchemaType(name = "positiveInteger")
    protected BigInteger ordering;
    @XmlAnyAttribute
    private Map<QName, String> otherAttributes = new HashMap<QName, String>();

    /**
     * Gets the value of the errorRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the errorRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getErrorRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getErrorRef() {
        if (errorRef == null) {
            errorRef = new ArrayList<EntityRef>();
        }
        return this.errorRef;
    }

    public boolean isSetErrorRef() {
        return ((this.errorRef!= null)&&(!this.errorRef.isEmpty()));
    }

    public void unsetErrorRef() {
        this.errorRef = null;
    }

    /**
     * Gets the value of the sportsLeg property.
     * 
     * @return
     *     possible object is
     *     {@link SportsLeg }
     *     
     */
    public SportsLeg getSportsLeg() {
        return sportsLeg;
    }

    /**
     * Sets the value of the sportsLeg property.
     * 
     * @param value
     *     allowed object is
     *     {@link SportsLeg }
     *     
     */
    public void setSportsLeg(SportsLeg value) {
        this.sportsLeg = value;
    }

    public boolean isSetSportsLeg() {
        return (this.sportsLeg!= null);
    }

    /**
     * Gets the value of the manualLeg property.
     * 
     * @return
     *     possible object is
     *     {@link ManualLeg }
     *     
     */
    public ManualLeg getManualLeg() {
        return manualLeg;
    }

    /**
     * Sets the value of the manualLeg property.
     * 
     * @param value
     *     allowed object is
     *     {@link ManualLeg }
     *     
     */
    public void setManualLeg(ManualLeg value) {
        this.manualLeg = value;
    }

    public boolean isSetManualLeg() {
        return (this.manualLeg!= null);
    }

    /**
     * Gets the value of the poolLeg property.
     * 
     * @return
     *     possible object is
     *     {@link PoolLeg }
     *     
     */
    public PoolLeg getPoolLeg() {
        return poolLeg;
    }

    /**
     * Sets the value of the poolLeg property.
     * 
     * @param value
     *     allowed object is
     *     {@link PoolLeg }
     *     
     */
    public void setPoolLeg(PoolLeg value) {
        this.poolLeg = value;
    }

    public boolean isSetPoolLeg() {
        return (this.poolLeg!= null);
    }

    /**
     * Gets the value of the lotteryLeg property.
     * 
     * @return
     *     possible object is
     *     {@link LotteryLeg }
     *     
     */
    public LotteryLeg getLotteryLeg() {
        return lotteryLeg;
    }

    /**
     * Sets the value of the lotteryLeg property.
     * 
     * @param value
     *     allowed object is
     *     {@link LotteryLeg }
     *     
     */
    public void setLotteryLeg(LotteryLeg value) {
        this.lotteryLeg = value;
    }

    public boolean isSetLotteryLeg() {
        return (this.lotteryLeg!= null);
    }

    /**
     * Gets the value of the noCombi property.
     * 
     * @return
     *     possible object is
     *     {@link NoCombi }
     *     
     */
    public NoCombi getNoCombi() {
        return noCombi;
    }

    /**
     * Sets the value of the noCombi property.
     * 
     * @param value
     *     allowed object is
     *     {@link NoCombi }
     *     
     */
    public void setNoCombi(NoCombi value) {
        this.noCombi = value;
    }

    public boolean isSetNoCombi() {
        return (this.noCombi!= null);
    }

    /**
     * Gets the value of the banker property.
     * 
     * @return
     *     possible object is
     *     {@link YesNo }
     *     
     */
    public YesNo getBanker() {
        return banker;
    }

    /**
     * Sets the value of the banker property.
     * 
     * @param value
     *     allowed object is
     *     {@link YesNo }
     *     
     */
    public void setBanker(YesNo value) {
        this.banker = value;
    }

    public boolean isSetBanker() {
        return (this.banker!= null);
    }

    /**
     * Gets the value of the result property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getResult() {
        return result;
    }

    /**
     * Sets the value of the result property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setResult(String value) {
        this.result = value;
    }

    public boolean isSetResult() {
        return (this.result!= null);
    }

    /**
     * Gets the value of the id property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getId() {
        return id;
    }

    /**
     * Sets the value of the id property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setId(String value) {
        this.id = value;
    }

    public boolean isSetId() {
        return (this.id!= null);
    }

    /**
     * Gets the value of the documentId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDocumentId() {
        return documentId;
    }

    /**
     * Sets the value of the documentId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDocumentId(String value) {
        this.documentId = value;
    }

    public boolean isSetDocumentId() {
        return (this.documentId!= null);
    }

    /**
     * Gets the value of the provider property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProvider() {
        if (provider == null) {
            return "OpenBet";
        } else {
            return provider;
        }
    }

    /**
     * Sets the value of the provider property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProvider(String value) {
        this.provider = value;
    }

    public boolean isSetProvider() {
        return (this.provider!= null);
    }

    /**
     * Gets the value of the addr property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAddr() {
        return addr;
    }

    /**
     * Sets the value of the addr property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAddr(String value) {
        this.addr = value;
    }

    public boolean isSetAddr() {
        return (this.addr!= null);
    }

    /**
     * Gets the value of the version property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getVersion() {
        return version;
    }

    /**
     * Sets the value of the version property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setVersion(String value) {
        this.version = value;
    }

    public boolean isSetVersion() {
        return (this.version!= null);
    }

    /**
     * Gets the value of the ordering property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getOrdering() {
        return ordering;
    }

    /**
     * Sets the value of the ordering property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setOrdering(BigInteger value) {
        this.ordering = value;
    }

    public boolean isSetOrdering() {
        return (this.ordering!= null);
    }

    /**
     * Gets a map that contains attributes that aren't bound to any typed property on this class.
     * 
     * <p>
     * the map is keyed by the name of the attribute and 
     * the value is the string value of the attribute.
     * 
     * the map returned by this method is live, and you can add new attribute
     * by updating the map directly. Because of this design, there's no setter.
     * 
     * 
     * @return
     *     always non-null
     */
    public Map<QName, String> getOtherAttributes() {
        return otherAttributes;
    }

}
