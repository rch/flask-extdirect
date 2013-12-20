

class BaseProvider(object):
    
    # TODO maybe change 'resource' parameter to 'model'
    
    def __init__(self, resource):
        
        super(BaseProvider, self).__init__()
        
        self._uri = None
        
        if hasattr(self, 'adapter'):
            self.resource = self.adapter.adapt(resource)
        else:
            self.resource = resource
        
        self.features = []
        if hasattr(resource, 'features'):
            provider = ResourceProvider()
            for feature in resource.features:
                if feature is not None:
                    try:
                        self.add_feature(provider(feature))
                    except NotImplementedError:
                        try:
                            for item in feature:
                                self.add_feature(provider(item))
                        except TypeError:
                            # added to support DZ_STATE feature from PT_DZSTATE
                            self.add_feature(provider(feature))
        
    
    def uri(self, uri=None):
        if uri is not None:
            self._uri = uri
        return self._uri
    
    def add_feature(self, feature):
        if feature not in self.features:
            self.features.append(feature)  


    def data_elements(self):
        lst = [] 
        for element in self.resource.data_element_index:
            lst.append(DataElementAdapter(element, resource))
        return lst
    
    
    def nodes(self, parents=set(), de_set_tags=None):
        
        if self in parents:
            return []
        
        root = {}
            
        for element in self.resource.data_element_index:
            if de_set_tags is None or element.tag in de_set_tags:
                de_adapter = DataElementAdapter(element, self.resource)
                node = de_adapter.adapt(DataNode)
                root[node.name] = node
                
            for extended_element in core_utils.extended_elements(element, self.resource):
                if extended_element is not None:
                    if de_set_tags is None or extended_element.tag in de_set_tags:
                        de_adapter = DataElementAdapter(extended_element, self.resource)
                        node = de_adapter.adapt(DataNode)
                        root[node.name] = node
        
        if len(root) > 0:
            lst = [root]
        else:
            lst = []
        
        parents.add(self)            
        for feature in self.features:
            ext = feature.nodes(de_set_tags=de_set_tags)
            if len(ext) > 0:
                lst.append(ext)
            
        return lst
