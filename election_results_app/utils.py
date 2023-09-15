def get_client_ip(request):
    """
    Get the my IP address using the os
    """
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # If the IP address is a list, return the first item
        if isinstance(ip, list):
            return ip[0]
        return ip
    except Exception as e:
        return None
