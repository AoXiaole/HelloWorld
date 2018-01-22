#ifndef __MOD_AS_PRESENCE_JSONV2_H__
#define __MOD_AS_PRESENCE_JSONV2_H__

//#include <switch.h>
//#include <switch_json.h>
#include <string>
#include <map>
#include <vector>

using namespace std;
// test define
	enum switch_status_t
	{
		SWITCH_STATUS_SUCCESS,
		SWITCH_STATUS_FALSE	
	};

enum CJSONTYPE
{
	cJSON_Empty,
	cJSON_Object,
	cJSON_String,
	cJSON_Number,
	cJSON_Array,
	cJSON_TypeMAX,

};
struct cJSON
{
	cJSON *next;
	cJSON *child;
	int type;
	int valueint;
	const char *valuestring;
	const char *string;
};

#define switch_log_printf(argc,...)
#define SWITCH_CHANNEL_LOG
#define SWITCH_LOG_ERROR
extern int cJSON_GetArraySize(cJSON *json);
extern void cJSON_Delete(cJSON *pjson);
extern cJSON *cJSON_Parse(const char *str);

//
class CJsonMapNd
{
public:    
    CJsonMapNd(const char *pStr);
    CJsonMapNd(int nInt);
	CJsonMapNd(CJsonMapNd & JsonMapNd);
    CJsonMapNd();
    virtual ~CJsonMapNd();
	switch_status_t EncodeJsonString(const char* pString);
	
    bool IsExist(const char *pKey);
	//bool IsExist();
	int Type();
	const char* TypeString();
    int Size();
	void SetSize(int nNums); // 设置数组列表的大小	
  	int SetInt(int nInt);
    int SetStr(const char *pStr);
    const char *Str();
    int Int();
    CJsonMapNd *Obj();
    switch_status_t EncodeJson(cJSON *pJson);
    CJsonMapNd& operator [](const char *pKey);
    CJsonMapNd& operator [](int nIndex); 
	CJsonMapNd& operator =(const char * pStr);
	CJsonMapNd& operator =(int nInt);
	CJsonMapNd& operator =(CJsonMapNd &jsonMapNd);
private:
	void Filling(CJsonMapNd &jsonMapNd);
	void Clear();
    union
    {
		string *m_pStr;
        int m_int;  
        map<string, CJsonMapNd *> *m_pMap;    // json <key ,value>
        struct
        {
            CJsonMapNd * pArrayObj;
            int nCount;
        }ARRAY;   //json array

		vector<CJsonMapNd *> *m_pList;
    }Data;
	
	
    int m_nType;

	static const char *m_pTypeString[cJSON_TypeMAX];
};

class CJsonMap
{
public:    
    virtual ~CJsonMap();
    switch_status_t EncodeJsonString(const char* pString);
    CJsonMapNd& operator [](const char *pKey);
	bool IsExist(const char *pKey);
	//bool IsExist();
private:
    CJsonMapNd m_jsonmapNode;
    cJSON *m_pjson;
};


class JsonObj
{
public:
		
	JsonObj(int nType = cJSON_Empty):m_nType(nType){}
	virtual ~JsonObj();
	virtual JsonObj& operator [](const char *pKey){throw "error"; return *(JsonObj* NULL);}
    virtual JsonObj& operator [](int nIndex){throw "error"; return *(JsonObj* NULL);} 
	virtual JsonObj& operator =(const char * pStr){throw "error"; return *(JsonObj* NULL)};
	virtual JsonObj& operator =(int nInt){throw "error"; return *(JsonObj* NULL)};
	virtual JsonObj& operator =(JsonObj &jsonObj){throw "error"; return *(JsonObj* NULL);}
	virtual int Int(){throw "error"; return 0;}
	virtual const char * Str(){throw "error"; return NULL;}
	virtual JsonObj& Obj(){return *this;}
	virtual int Type(){return m_nType;}
private:
	int m_nType;
	JsonObj *pJsonObj;
	
};

class JsonInt:public JsonObj
{
public:
	JsonInt();
	JsonInt(int nInt);
	~JsonInt();
	int Int();
	JsonObj& operator =(int nInt);
private:
	int m_value;
};

class JsonString:public JsonObj
{
public:
	JsonString();
	JsonString(const char *pStr);
	~JsonString();
	const char * Str();
	JsonObj& operator =(const char * pStr);
private:
	string m_value;
};

class JsonMap:public JsonObj
{
public:
	JsonMap();
//	JsonMap(const char *pStr);
	~JsonMap();
	JsonObj& operator [](const char *pKey);
	JsonObj& operator =(JsonObj &jsonObj);
private:
	map<string, JsonObj *> m_value;
};

class JsonArray: public JsonObj
{
public:
	JsonArray();
//	JsonMap(const char *pStr);
	~JsonArray();
	JsonObj& operator [](int nIndex);
	JsonObj& operator =(JsonObj &jsonObj);

	
private:
	vector<JsonObj *> m_value;
};

#endif

