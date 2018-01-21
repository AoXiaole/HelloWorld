#include"mod_as_presence_json_v2.h"

const char * CJsonMapNd::m_pTypeString[cJSON_TypeMAX] = {
	"cJSON_Empty",
	"cJSON_Object",
	"cJSON_String",
	"cJSON_Number",
	"cJSON_Array"
	};

CJsonMapNd::CJsonMapNd(const char *pStr)
{
    m_nType = cJSON_String; 
    Data.m_pStr = new string(pStr); 
}

CJsonMapNd::CJsonMapNd(int nInt)
{
    m_nType = cJSON_Number; 
    Data.m_int = nInt; 
}

CJsonMapNd::CJsonMapNd(CJsonMapNd & JsonMapNd)
{
	Filling(JsonMapNd);
}

CJsonMapNd:: CJsonMapNd()
{
    m_nType = cJSON_Empty;
}

CJsonMapNd::~CJsonMapNd()
{
    Clear();
}

void CJsonMapNd::Clear()
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
		int size = Data.m_pList->size();
		for(int i = 0; i < size; i++)
		{
			if(NULL != (*Data.m_pList)[i])
			{
				delete (*Data.m_pList)[i];
			}
		}
			
		delete Data.m_pList;
	}
	else if(cJSON_String == m_nType)
	{
		delete Data.m_pStr;
	}

}

void CJsonMapNd::Filling(CJsonMapNd &JsonMapNd)
{	
	m_nType = JsonMapNd.m_nType;
	switch(m_nType)
	{
		case cJSON_Number:
		{
			Data.m_int = JsonMapNd.Data.m_int;
			break;
		}
		case cJSON_String:
		{
			Data.m_pStr = new string(*(JsonMapNd.Data.m_pStr));
			break;
		}
		case cJSON_Object:
		{
			Data.m_pMap = new  map<string, CJsonMapNd *>(*(JsonMapNd.Data.m_pMap));
			map<string, CJsonMapNd *>::iterator it = Data.m_pMap->begin();
			for(; it != Data.m_pMap->end(); it++)
			{
				if(it->second)
				{
					it->second = new CJsonMapNd(*(it->second));
				}
			}
			break;
		} 
		case cJSON_Array:
		{
			Data.m_pList = new vector<CJsonMapNd *>(*(JsonMapNd.Data.m_pList));
			int size = Data.m_pList->size();
			for(int i = 0; i < size; i++)
			{
				if(NULL != (*Data.m_pList)[i])
				{
					(*Data.m_pList)[i] = new CJsonMapNd(*((*Data.m_pList)[i]));
				}
			}
			break;
		}
		case cJSON_Empty:
		{
			break;
		}
		default:
		{
			break;
		}
			
	}
	
}


switch_status_t CJsonMapNd::EncodeJsonString(const char* pString)
{

	cJSON *m_pjson;	
	switch_status_t nRet = SWITCH_STATUS_FALSE;
	if(NULL == pString || NULL == (m_pjson = cJSON_Parse(pString))) 
	{
	    return SWITCH_STATUS_FALSE;
	}

	nRet = EncodeJson(m_pjson);
	cJSON_Delete(m_pjson);
	
	return nRet;
}


bool CJsonMapNd::IsExist(const char *pKey)
{
	bool bRet = false;
	
    if(this != NULL && cJSON_Object == m_nType)
    {
	    map<string, CJsonMapNd *>::iterator it = Data.m_pMap->find(pKey);
	    if( it != Data.m_pMap->end())
	    {
	        bRet = true;
	    }
    } 
	return bRet;
}

/*
bool CJsonMapNd::IsExist()
{
	bool bRet = false;
	
    if(this != NULL)
    {
		bRet = true;
    } 
	return bRet;
}*/

int CJsonMapNd::Type()
{
	return m_nType;
}

const char * CJsonMapNd::TypeString()
{
	return m_pTypeString[m_nType];
}
int CJsonMapNd::Size()
{
	//return Data.ARRAY.nCount;
	if(cJSON_Array == m_nType)
	{
		return Data.m_pList->size();
	}
	else
	{
		return 0;
	}
}

void CJsonMapNd::SetSize(int nNums)
{
	//return Data.ARRAY.nCount;
	if(cJSON_Array == m_nType)
	{
		Data.m_pList->resize(nNums);
	}
	else if(cJSON_Empty == m_nType)
	{
		m_nType = cJSON_Array; 
		Data.m_pList = new vector<CJsonMapNd *>(nNums, NULL);
	}
		
}

const char *CJsonMapNd::Str()
{
    if(this && cJSON_String == m_nType) 
    {
        return Data.m_pStr->c_str();
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
		int nCount = cJSON_GetArraySize(pJson);
       // Data.ARRAY.nCount = cJSON_GetArraySize(pJson);
        //Data.ARRAY.pArrayObj = new CJsonMapNd[Data.ARRAY.nCount]();
		Data.m_pList = new vector<CJsonMapNd *>(nCount, NULL);
        while(c && (i < nCount))
        {
           // Data.ARRAY.pArrayObj[i].EncodeJson(c);
           	(*Data.m_pList)[i] = new CJsonMapNd();
		   	(*Data.m_pList)[i]->EncodeJson(c);
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
                    pChildJson = new CJsonMapNd();
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

	CJsonMapNd& jsonmapNd = *(CJsonMapNd *)NULL;
	
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
            jsonmapNd = *(it->second);
        }
        else
        {
			CJsonMapNd *pChildJson = new CJsonMapNd();
			(*Data.m_pMap)[pKey] = pChildJson;            
            jsonmapNd = *pChildJson;
        }
    }
	else if(cJSON_Empty == m_nType)
	{
		CJsonMapNd *pChildJson = new CJsonMapNd();
		m_nType = cJSON_Object;
		Data.m_pMap = new map<string, CJsonMapNd *>();
		
		(*Data.m_pMap)[pKey] = pChildJson;
		jsonmapNd = *pChildJson;
		
	}
    else
    {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator [](const char *pKey)  pkey = %s ,type =  %s\n", pKey, TypeString);
        jsonmapNd = *(CJsonMapNd *)NULL;
    }
	
	return jsonmapNd;
}

CJsonMapNd& CJsonMapNd::operator [](int nIndex)
{
	int nListSize = 0;
	CJsonMapNd& jsonmapNd = *(CJsonMapNd *)NULL;
	
    if(this == NULL )
    {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator [](int nIndex) this == NULL\n");
        return *(CJsonMapNd *)NULL;
    }
    
    if(cJSON_Array == m_nType)		
    {
    	if(nIndex >= Data.m_pList->size())
        {
        	Data.m_pList->resize(nIndex + 1);
    	}
		if(NULL == (*Data.m_pList)[nIndex])
		{
			(*Data.m_pList)[nIndex] =  new CJsonMapNd();
		}
		jsonmapNd =  *((*Data.m_pList)[nIndex]);
    }
	else if(cJSON_Empty == m_nType)
	{
		m_nType = cJSON_Array; 
		Data.m_pList = new vector<CJsonMapNd *>(nIndex + 1, NULL);
		(*Data.m_pList)[nIndex] =  new CJsonMapNd();
		jsonmapNd = *((*Data.m_pList)[nIndex]);
	}
	else
    {
        switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator [](int nIndex) type = %s , index = %d\n", TypeString, nIndex,  cJSON_Array == m_nType ? Data.m_pList->size() :0);
        jsonmapNd = *(CJsonMapNd *)NULL;
    }
	return jsonmapNd;
}


CJsonMapNd& CJsonMapNd::operator =(const char * pStr)
{
	if(cJSON_String == m_nType)
	{
		(*Data.m_pStr) = pStr;
	}
	else if(cJSON_Empty == m_nType)
	{
		m_nType = cJSON_String;
		Data.m_pStr = new string(pStr);
	}
	else
	{
		switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator =(const char * pStr) pStr = %s, type = %s \n", pStr, TypeString);
	}
	
	return *this;	
}
CJsonMapNd& CJsonMapNd::operator =(int n_int)
{
	if(cJSON_Number == m_nType)
	{
		Data.m_int = n_int;
	}
	else if(cJSON_Empty == m_nType)
	{
		m_nType = cJSON_Number;
		Data.m_int = n_int;
	}
	else
	{
		switch_log_printf(SWITCH_CHANNEL_LOG, SWITCH_LOG_ERROR, "CJsonMapNd::operator =(int n_int) n_int = %d, type = %s \n", n_int, TypeString);
	}
	
	return *this;
}
CJsonMapNd& CJsonMapNd::operator =(CJsonMapNd & jsonMapNd)
{
	Clear();
	Filling(jsonMapNd);
	
	return *this;
}



CJsonMap::~CJsonMap()
{
    if(m_pjson)
    {
         cJSON_Delete(m_pjson);
    }
}

switch_status_t CJsonMap::EncodeJsonString(const char* pString)
{
  if(NULL == pString || NULL == (m_pjson = cJSON_Parse(pString))) 
  {
        return SWITCH_STATUS_FALSE;
  }
  
  return m_jsonmapNode.EncodeJson(m_pjson);
}

CJsonMapNd& CJsonMap::operator [](const char *pKey)
{
    if(NULL == pKey)
    {
        return *(CJsonMapNd *)NULL;
    }
    return m_jsonmapNode[pKey];
}

bool CJsonMap::IsExist(const char *pKey)
{
	return m_jsonmapNode.IsExist(pKey);
}

/*
bool CJsonMap::IsExist()
{
	return true;
}*/



