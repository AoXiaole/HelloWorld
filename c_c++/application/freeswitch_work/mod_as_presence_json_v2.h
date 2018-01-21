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

#endif
