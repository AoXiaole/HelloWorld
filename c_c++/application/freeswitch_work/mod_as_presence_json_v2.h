#ifndef __MOD_AS_PRESENCE_JSONV2_H__
#define __MOD_AS_PRESENCE_JSONV2_H__

#include <switch.h>
#include <switch_json.h>
#include <string>
#include <map>
using namespace std;

class CJsonMapNd
{
public:    
    CJsonMapNd(const char *pStr);
    CJsonMapNd(int nInt);
    CJsonMapNd();
    virtual ~CJsonMapNd();
    bool IsExist();
    
//    int SetInt(int nInt){ Data.m_int = nInt;}
//    int SetStr(const char *pStr){ Data.m_pStr = pStr;}
    const char *Str();
    int Int();
    CJsonMapNd *Obj();
    switch_status_t EncodeJson(cJSON *pJson);
    CJsonMapNd& operator [](const char *pKey);
    CJsonMapNd& operator [](int nIndex); 
private:
    union
    {
        const char *m_pStr;
        int m_int;  
        map<string, CJsonMapNd *> *m_pMap;    // json <key ,value>
        struct
        {
            CJsonMapNd * pArrayObj;
            int nCount;
        }ARRAY;   //json array
    }Data;
    
    int m_nType;
};

class CJsonMap
{
public:    
    virtual ~CJsonMap();
    switch_status_t EncodeJsonString(const char* pString);
    CJsonMapNd& operator [](const char *pKey);
private:
    CJsonMapNd m_jsonmapNode;
    cJSON *m_pjson;
};

#endif
