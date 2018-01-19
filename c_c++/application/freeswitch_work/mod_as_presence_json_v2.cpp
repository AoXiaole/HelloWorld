#include"mod_as_presence_json_v2.h"
CJsonMapNd::CJsonMapNd(const char *pStr)
{
    m_nType = cJSON_String; 
    Data.m_pStr = pStr; 
}

CJsonMapNd::CJsonMapNd(int nInt)
{
    m_nType = cJSON_Number; 
    Data.m_int = nInt; 
}

CJsonMapNd:: CJsonMapNd()
{
    m_nType = cJSON_Object;
}

CJsonMapNd::~CJsonMapNd()
{
    if(cJSON_Object == m_nType)
    {
        if(Data.m_pMap)
        {
            map<string, CJsonMapNd *>::iterator it = Data.m_pMap->begin();
            for(; it != Data.m_pMap->end(); it++)
            {
                if(it->second)
                {
                    delete it->second;
                }
            }
            delete Data.m_pMap;
        }
    }
    else if(cJSON_Array == m_nType)
    {
        if(Data.ARRAY.pArrayObj)
        {
            delete [] Data.ARRAY.pArrayObj;
        }
    }
}

bool CJsonMapNd::IsExist()
{
    if(this != NULL)
    {
        return true;
    }
    else
    {
        return false;
    }
}

const char *CJsonMapNd::Str()
{
    if(this && cJSON_String == m_nType) 
    {
        return Data.m_pStr;
    }
    else
    {
        throw "get str error";
    }
}

int CJsonMapNd::Int()
{
    if(this && cJSON_Number == m_nType) 
    {
        return Data.m_int;
    }
    else
    {
        throw "get int error";
    }
}

CJsonMapNd *CJsonMapNd::Obj()
{
    return this;
}

switch_status_t CJsonMapNd::EncodeJson(cJSON *pJson)
{
    switch_status_t nRet = SWITCH_STATUS_SUCCESS;
    if(NULL == pJson)
    {
        return SWITCH_STATUS_FALSE;
    }
    
    m_nType = pJson->type;
    if(cJSON_Array == pJson->type)
    {
        cJSON *c = pJson->child; 
        int i = 0;
        Data.ARRAY.nCount = cJSON_GetArraySize(pJson);
        Data.ARRAY.pArrayObj = new CJsonMapNd[Data.ARRAY.nCount]();
        while(c && (i < Data.ARRAY.nCount))
        {
            Data.ARRAY.pArrayObj[i].EncodeJson(c);
            i++;
            c = c->next;
        }
    }
    else if(cJSON_Object == pJson->type)
    {
        cJSON *c = pJson->child; 
        CJsonMapNd *pChildJson = NULL;
        Data.m_pMap = new map<string, CJsonMapNd *>();
        while(c)
        {
            
            switch(c->type)
            {
                case cJSON_Object:
                    pChildJson = new CJsonMapNd(cJSON_Object);
                    nRet = pChildJson->EncodeJson(c);
                    break;
                    
                case cJSON_String:
                    pChildJson = new CJsonMapNd(c->valuestring);
                    break;
                    
                case cJSON_Number:
                    pChildJson = new CJsonMapNd(c->valueint);
                    break;
                    
                case cJSON_Array:
                    pChildJson = new CJsonMapNd();
                    nRet = pChildJson->EncodeJson(c);
                    break;
                //  TODO: 其他类型未完成
                default :
                   
                    nRet = SWITCH_STATUS_FALSE;
            }
            if(SWITCH_STATUS_FALSE == nRet)
            {
                break;
            }
            
            (*Data.m_pMap)[c->string] = pChildJson;
            c = c->next;
        }
    }
    return nRet;
}


CJsonMapNd& CJsonMapNd::operator [](const char *pKey)
{
    if( NULL == this || NULL == pKey)
    {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator [](const char *pKey), this = %p , pKey = %p\n", this , pKey);
        return *(CJsonMapNd *)NULL;
    }
    
    if(cJSON_Object == m_nType)
    {
        map<string, CJsonMapNd *>::iterator it = Data.m_pMap->find(pKey);
        if( it != Data.m_pMap->end())
        {
            return *(it->second);
        }
        else
        {
            switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, " CJsonMapNd::operator [](const char *pKey), pKey = %s,find = NULL\n", pKey);
            return *(CJsonMapNd *)NULL;
        }
    }
    else
    {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator [](const char *pKey)  pkey = %s is not JsonObj\n", pKey);
        return *(CJsonMapNd *)NULL;
    }
}

CJsonMapNd& CJsonMapNd::operator [](int nIndex)
{
    if(this == NULL )
    {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator [](int nIndex) this == NULL\n");
        return *(CJsonMapNd *)NULL;
    }
    
    if(cJSON_Array == m_nType && nIndex < Data.ARRAY.nCount)
    {
        return Data.ARRAY.pArrayObj[nIndex];
    }
    else
    {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator [](int nIndex) type = %d , index = %d, nCount = %d \n",m_nType, nIndex ,Data.ARRAY.nCount );
        return *(CJsonMapNd *)NULL;
    }
}

CJsonMap::~CJsonMap()
{
    if(pjson)
    {
         cJSON_Delete(pjson);
    }
}

switch_status_t CJsonMap::EncodeJsonString(const char* pString)
{
  if(NULL == string || NULL == (m_pjson = cJSON_Parse(pString))) 
  {
        return SWITCH_STATUS_FALSE;
  }
  
  return JsonBase.EncodeJson(m_pjson);
}

CJsonMapNd& CJsonMap::operator [](const char *pKey)
{
    if(NULL == pKey)
    {
        return *(CJsonMapNd *)NULL;
    }
    return m_jsonmapNode[pKey];
}

