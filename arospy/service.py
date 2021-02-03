import asyncio
import functools
import threading
import logging
import typing
import rospy


_logger = logging.getLogger("arospy.service")


class ServiceProxy:
    """
    Asynchronous ROS service proxy (client).
    """
    def __init__(self, name: str, service_class, persistent: bool = False, headers=None):
        self.inner = rospy.ServiceProxy(name, service_class, persistent=persistent, headers=headers)
        self.event_loop = asyncio.get_event_loop()

    async def wait_for_service(self, timeout=None):
        await self.event_loop.run_in_executor(None, self.inner.wait_for_service, timeout)

    async def call(self, *args, **kwargs):
        return await self.event_loop.run_in_executor(None, functools.partial(self.inner.call, *args, **kwargs))


class Service:
    """
    Asynchronous ROS service server.
    You can use classic rospy.Service, but if you want communication between the service handler and your coroutines,
    you can use this class.
    """
    def __init__(self, name: str,
                 service_class,
                 handler: typing.Callable[[typing.Any], typing.Awaitable[typing.Any]],
                 buff_size=rospy.topics.DEFAULT_BUFF_SIZE):
        """
        :param name:
        :param service_class:
        :param handler: Async callback to handle the requests
        :param buff_size:
        """
        self.inner = rospy.Service(name, service_class, handler=self._handle_request, buff_size=buff_size)
        self.handler = handler
        self.event_loop = asyncio.get_event_loop()

    def _handle_request(self, request):
        _logger.debug(f"Service {self.inner.resolved_name} received request {request} in thread {threading.get_ident()}")
        future = asyncio.run_coroutine_threadsafe(self.handler(request), loop=self.event_loop)
        return future.result()
