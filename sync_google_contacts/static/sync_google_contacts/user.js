		$(document).ready(function () {
			$('#UserMngt').jtable({
			title: 'Manage users/groups',
			paging: false, //Enable paging
			pageSize: 10, //Set page size (default: 10)
			sorting: true, //Enable sorting
			create: true,
			edit:true,
			defaultSorting: 'Id DESC', //Set default sorting
			actions: {
				listAction: '/groupmanagement/ajax/user-m/display/',
				createAction: '/groupmanagement/ajax/user-m/add/',
				updateAction: '/groupmanagement/ajax/user-m/update/',
				deleteAction: '/groupmanagement/ajax/user-m/delete/'
			},
			fields: {
				'Id': {
				key: true,
				list: false,
				create: false,
				hidden: true,
				},

                Groups: {
                    title: 'attached groups',
                    width: '5%',
                    sorting: false,
                    edit: false,
                    create: false,
                    display: function (userData) {
                        //Create an image that will be used to open child table
						html = '<img src="'+STATIC_URL+'group_user_mngt/contact-list-icon.png">';
                        var $img = $(html);
                        //Open child table when user clicks the image
                        $img.click(function () {
                            $('#UserMngt').jtable('openChildTable',
                                    $img.closest('tr'),
                                    {
                                        title: userData.record.email + ' - Attached groups',
										sorting: true,
                                        actions: {
                                            listAction: '/groupmanagement/ajax/group-s/display/'+userData.record.email,
                                            deleteAction: '/groupmanagement/ajax/group-s/delete/'+userData.record.email,
                                            createAction: '/groupmanagement/ajax/group-s/add/'+userData.record.email
                                        },
                                        fields: {
                                            'Id': {
												key: true,
                                                list: false,
												create: false,
												hidden: true,
                                            },
                                            'name': {
												title : 'group name',
                                                key: false,
                                                edit: false,
												create: true,
												display: function (data) { return data.record.name;},
												options: function (data) {
													data.clearCache()
													return '/groupmanagement/ajax/group-s/index/'+userData.record.email ; }
                                            },
                                        }
                                    }, function (data) { //opened handler
                                        data.childTable.jtable('load');
                                    });
                        });
                        //Return image to show on the person row
                        return $img;
                    }
                },

				'email': {
				title: 'email',
				edit: true,
				width: '20%'
				},
				'active': {
				title : 'status',
				width: '10%',
				edit: true,
				type: 'checkbox',
				values: { 'false': 'Not active', 'true': 'Active' },
				},
				'password': {
				title : 'password',
				edit: true,
				create: true,
				list: false,
				type: 'password',
				},
				'lastname': {
					title : 'last name',
					key: false,
					edit: true,
					create: true,
				},
				'firstname': {
					title : 'firstname',
					key: false,
					edit: true,
					create: true,
				},
				'is_staff': {
					title : 'is staff',
					width: '5%',
					key: false,
					edit: true,
					create: true,
					type: 'checkbox',
					values: { 'false': 'No', 'true': 'Yes' },
				},
				'is_superuser': {
					title : 'is superuser',
					width: '5%',
					key: false,
					edit: true,
					create: true,
					type: 'checkbox',
					values: { 'false': 'No', 'true': 'Yes' },
				},
				'last_login': {
					title: 'last login',
					width: '30%',
					edit: false,
					create: false,
				},
				'date_joined': {
					title: 'date joined',
					width: '30%',
					edit: false,
					create: false,
				},


			}
			});
		$('#UserMngt').jtable('load');
		});
